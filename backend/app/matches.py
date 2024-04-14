from app import schemas
from app.models import User


def jaccard_similarity(list1: list, list2: list) -> float:
    """
    Calculates the Jaccard similarity coefficient between two lists.

    The Jaccard similarity coefficient is a measure of the similarity between two sets.
    It is defined as the size of the intersection divided by the size of the union of the sets.

    Args:
        list1 (list): The first list.
        list2 (list): The second list.

    Returns:
        float: The Jaccard similarity coefficient between the two lists.
    """
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))


def get_similarity_score(current_user: User, other_user: schemas.UserMatch) -> float:
    """
    Calculates the similarity score between two users based on their attributes.

    Args:
        current_user (User): The current user.
        other_user (schemas.UserMatch): The other user to compare with.

    Returns:
        float: The similarity score between the two users.
    """
    MAX_SKILLS_PREF_SCORE = 4
    MAX_COMMON_SKILLS_SCORE = 2
    MAX_AGE_DIFF_SCORE = 1
    MAX_SAME_GENDER_SCORE = 0.5
    MAX_SAME_COUNTRY_SCORE = 1
    MAX_COMMON_HOBBIES_SCORE = 1

    score = 0

    # The more skills the other user has that match the current user's skills preferences,
    # the higher the score
    user_skills_pref = set(current_user.preferred_skills)
    score += (
        len(user_skills_pref & set(other_user.skills)) / len(user_skills_pref)
    ) * MAX_SKILLS_PREF_SCORE

    # Common skills are weighted more heavily than common hobbies
    score += (
        jaccard_similarity(current_user.skills, other_user.skills)
        * MAX_COMMON_SKILLS_SCORE
    )

    # NOTE: As long as the age difference is less than 100 years, the score will be between 0 and 1
    score += MAX_AGE_DIFF_SCORE - (
        abs(current_user.dob.year - other_user.dob.year) / 100
    )

    # Give higher preference to users with the same gender
    score += MAX_SAME_GENDER_SCORE if current_user.gender == other_user.gender else 0

    # Give higher score if users are from the same country
    score += MAX_SAME_COUNTRY_SCORE if current_user.country == other_user.country else 0

    score += (
        jaccard_similarity(current_user.hobbies, other_user.hobbies)
        * MAX_COMMON_HOBBIES_SCORE
    )

    # Normalize the score to be between 0 and 1
    total_max_score = (  # Maximum possible score
        MAX_SKILLS_PREF_SCORE
        + MAX_COMMON_SKILLS_SCORE
        + MAX_AGE_DIFF_SCORE
        + MAX_SAME_GENDER_SCORE
        + MAX_SAME_COUNTRY_SCORE
        + MAX_COMMON_HOBBIES_SCORE
    )
    score /= total_max_score

    return score


def rank_matches(
    current_user: User, matches: list[schemas.UserMatch]
) -> list[schemas.UserMatch]:
    matches.sort(
        key=lambda user: get_similarity_score(current_user, user), reverse=True
    )
    return matches
