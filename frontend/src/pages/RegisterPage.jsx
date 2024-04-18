import { useEffect, useState } from "react";
import { Button, Col, Form, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import Select from "react-select";
import CreatableSelect from "react-select/creatable";
import { toast } from "react-toastify";
import { FormContainer, Loader } from "../components";
import {
  hobbyOptions,
  languageOptions,
  skillProficiencyOptions,
} from "../data";
import { setCredentials } from "../slices/authSlice";
import { useRegisterMutation } from "../slices/usersApiSlice";
import { FancyHeading } from "../styles/FancyHeading";

const RegisterPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [fullname, setFullname] = useState("");
  const [bio, setBio] = useState("");
  const [profileImage, setProfileImage] = useState(null);
  const [dob, setDob] = useState("");
  const [gender, setGender] = useState("Male");
  const [country, setCountry] = useState("");
  const [city, setCity] = useState("");
  const [githubProfile, setGithubProfile] = useState("");
  const [linkedinProfile, setLinkedinProfile] = useState("");
  const [skillProficiencies, setSkillProficiencies] = useState([]);
  const [highestEducation, setHighestEducation] = useState("");
  const [experienceYears, setExperienceYears] = useState(0);
  const [languages, setLanguages] = useState([]);
  const [goal, setGoal] = useState("Build Projects");
  const [commitmentHours, setCommitmentHours] = useState(0);
  const [hobbies, setHobbies] = useState([]);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [register, { isLoading }] = useRegisterMutation();

  const { userInfo } = useSelector((state) => state.auth);

  useEffect(() => {
    if (userInfo) {
      navigate("/");
    }
  }, [navigate, userInfo]);

  const submitHandler = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
    } else {
      try {
        let cleanedGithubProfile = githubProfile.replace(/\/$/, "");
        setProfileImage(cleanedGithubProfile + ".png");

        let userData = {
          email: email,
          password: password,
          full_name: fullname,
          bio: bio,
          profile_image: profileImage,
          date_of_birth: dob,
          gender: gender,
          country: country,
          city: city,
          github_profile: githubProfile,
          linkedin_profile: linkedinProfile,
          skill_proficiencies: skillProficiencies,
          highest_education: highestEducation,
          experience_years: experienceYears,
          hobbies: hobbies,
          languages: languages,
          goal: goal,
          commitment_hours: commitmentHours,
        };
        console.log(userData);

        const res = await register(userData).unwrap();
        dispatch(setCredentials({ ...res }));
        navigate("/");
      } catch (err) {
        toast.error(err?.data?.message || err.error);
      }
    }
  };

  return (
    <FormContainer>
      <h1>
        <FancyHeading>Sign Up</FancyHeading>
      </h1>

      <Form onSubmit={submitHandler}>
        <Form.Group className="my-4" controlId="email">
          <Form.Label>Email Address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="confirmPassword">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Confirm password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="fullname">
          <Form.Label>Full Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter full name"
            value={fullname}
            onChange={(e) => setFullname(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="bio">
          <Form.Label>Bio</Form.Label>
          <Form.Control
            as="textarea"
            placeholder="Enter bio"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="dob">
          <Form.Label>Date of Birth</Form.Label>
          <Form.Control
            type="date"
            value={dob}
            onChange={(e) => setDob(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="gender">
          <Form.Label>Gender</Form.Label>
          <Form.Select
            aria-label="Gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            required
          >
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="my-4" controlId="country">
          <Form.Label>Country</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter country"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="city">
          <Form.Label>City</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter city"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="githubProfile">
          <Form.Label>GitHub Profile Link</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter GitHub Link"
            value={githubProfile}
            onChange={(e) => setGithubProfile(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="linkedinProfile">
          <Form.Label>LinkedIn Profile Link</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter LinkedIn username"
            value={linkedinProfile}
            onChange={(e) => setLinkedinProfile(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="skills">
          <Form.Label>Select your skills and expertise level</Form.Label>
          <Select
            options={skillProficiencyOptions}
            isMulti
            required
            onChange={(opt) => setSkillProficiencies(opt.map((o) => o.value))}
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="highestEducation">
          <Form.Label>Enter your Highest Educational Qualification</Form.Label>
          <Form.Control
            type="text"
            placeholder="Highest Education"
            value={highestEducation}
            onChange={(e) => setHighestEducation(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="experienceYears">
          <Form.Label>Number of years of Coding Experience</Form.Label>
          <Form.Control
            type="number"
            placeholder="Experience in years"
            value={experienceYears}
            onChange={(e) => setExperienceYears(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="hobbies">
          <Form.Label>List Your Hobbies</Form.Label>
          <CreatableSelect
            options={hobbyOptions}
            isMulti
            onChange={(opt) => setHobbies(opt.map((o) => o.value))}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="languages">
          <Form.Label>Enter the Languages You Speak</Form.Label>
          <CreatableSelect
            options={languageOptions}
            isMulti
            onChange={(opt) => setLanguages(opt.map((o) => o.value))}
            required
          />
        </Form.Group>

        <Form.Group className="my-4" controlId="goal">
          <Form.Label>Your Goal</Form.Label>
          <Form.Select
            aria-label="Gender"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            required
          >
            <option value="Build Projects">Build Projects</option>
            <option value="Prepare for Coding Interviews">
              Prepare for Coding Interviews
            </option>
            <option value="Both">Both</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="my-4" controlId="commitmentHours">
          <Form.Label>Number of hours you can commit per week</Form.Label>
          <Form.Control
            type="number"
            placeholder="Commitment Hours"
            value={commitmentHours}
            onChange={(e) => setCommitmentHours(e.target.value)}
            required
          />
        </Form.Group>

        <Button type="submit" variant="primary" className="mt-3">
          Sign Up
        </Button>
      </Form>

      {isLoading && <Loader />}

      <Row className="py-3">
        <Col>
          Already have an account? <Link to={`/login`}>Login</Link>
        </Col>
      </Row>
    </FormContainer>
  );
};

export default RegisterPage;
