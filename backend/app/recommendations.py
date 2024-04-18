from datetime import datetime

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy.orm import Session

from app import schemas
from app.core.db import engine
from app.models import User


def calculate_age(born):
    today = datetime.now()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def jaccard_index(a, b):
    intersection = len(set(a).intersection(set(b)))
    union = len(set(a).union(set(b)))
    return intersection / union


def encode_skills(skills):
    """
    Encodes a list of skills with their proficiency levels into a dictionary.
    """
    PROFICIENCY_MAPPING = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3,
    }

    skill_dict = {}
    for skill in skills:
        name, proficiency = skill.split(" - ")
        skill_dict[name] = PROFICIENCY_MAPPING[proficiency]
    return skill_dict


def vectorize_skills(skill_dict1, skill_dict2):
    """
    Vectorizes two skill dictionaries into two lists of skill levels.
    """
    master_list = set(skill_dict1.keys()).union(skill_dict2.keys())
    vector1 = [skill_dict1.get(skill, 0) for skill in master_list]
    vector2 = [skill_dict2.get(skill, 0) for skill in master_list]
    return vector1, vector2


def calculate_cosine_similarity(user1_skills, user2_skills):
    """
    Calculates the cosine similarity between two users' skills.
    """
    user1_skill_dict = encode_skills(user1_skills)
    user2_skill_dict = encode_skills(user2_skills)
    vector1, vector2 = vectorize_skills(user1_skill_dict, user2_skill_dict)
    return cosine_similarity([vector1], [vector2])[0][0]


def get_buddy_recommendations(
    current_user: User, session: Session
) -> list[schemas.UserMatch]:
    sql_query = f"""
    SELECT id, date_of_birth, country, city, skill_proficiencies, experience_years, hobbies, languages, goal, commitment_hours
    FROM users
    WHERE id != {current_user.id} AND
    ARRAY{current_user.languages}::varchar[] && languages;
    """

    other_users = pd.read_sql_query(sql_query, engine)

    min_max_scaler = MinMaxScaler()

    other_users["date_of_birth"] = pd.to_datetime(other_users["date_of_birth"])
    other_users["age"] = (datetime.now() - other_users["date_of_birth"]).dt.days // 365
    other_users["age_diff"] = abs(
        calculate_age(current_user.date_of_birth) - other_users["age"]
    )
    other_users["age_diff"] = min_max_scaler.fit_transform(other_users[["age_diff"]])
    other_users["age_score"] = 1 - other_users["age_diff"]

    other_users["location_score"] = 0.4 * (
        current_user.country == other_users["country"]
    ) + 0.6 * (current_user.city == other_users["city"])

    other_users["experience_diff"] = abs(
        current_user.experience_years - other_users["experience_years"]
    )
    other_users["experience_diff"] = min_max_scaler.fit_transform(
        other_users[["experience_diff"]]
    )
    other_users["experience_score"] = 1 - other_users["experience_diff"]

    other_users["hobbies_score"] = other_users["hobbies"].apply(
        lambda hobbies: jaccard_index(current_user.hobbies, hobbies)
    )

    other_users["languages_score"] = other_users["languages"].apply(
        lambda languages: jaccard_index(current_user.languages, languages)
    )

    other_users["goal_score"] = (current_user.goal == other_users["goal"]) + 0.5 * (
        (current_user.goal == "both") | (other_users["goal"] == "both")
    )

    other_users["commitment_hours_diff"] = abs(
        current_user.commitment_hours - other_users["commitment_hours"]
    )
    other_users["commitment_hours_diff"] = min_max_scaler.fit_transform(
        other_users[["commitment_hours_diff"]]
    )
    other_users["commitment_hours_score"] = 1 - other_users["commitment_hours_diff"]

    other_users["skills_score"] = other_users["skill_proficiencies"].apply(
        lambda skill_proficiencies: calculate_cosine_similarity(
            current_user.skill_proficiencies, skill_proficiencies
        )
    )

    other_users["similarity_score"] = (
        other_users["age_score"]
        + other_users["location_score"]
        + other_users["experience_score"]
        + other_users["hobbies_score"]
        + other_users["languages_score"]
        + other_users["goal_score"]
        + other_users["commitment_hours_score"]
        + other_users["skills_score"]
    )
    other_users["similarity_score"] = min_max_scaler.fit_transform(
        other_users[["similarity_score"]]
    )

    recommended_user_ids = (
        other_users.sort_values(by="similarity_score", ascending=False)
        .head(30)["id"]
        .tolist()
    )

    return session.query(User).filter(User.id.in_(recommended_user_ids)).all()
