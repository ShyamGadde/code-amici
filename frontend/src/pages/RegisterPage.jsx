import { useEffect, useState } from "react";
import { Button, Col, Form, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { FormContainer, Loader, PillInputList } from "../components";
import { setCredentials } from "../slices/authSlice";
import { useRegisterMutation } from "../slices/usersApiSlice";

const RegisterPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [fullname, setFullname] = useState("");
  const [bio, setBio] = useState(null);
  const [profilePictureUrl, setProfilePictureUrl] = useState(null);
  const [dob, setDob] = useState("");
  const [gender, setGender] = useState("Male");
  const [githubUsername, setGithubUsername] = useState("");
  const [linkedinUsername, setLinkedinUsername] = useState("");
  const [skills, setSkills] = useState([]);
  const [country, setCountry] = useState("");
  const [hobbies, setHobbies] = useState([]);
  const [preferredBuddyType, setPreferredBuddyType] = useState("Buddy");
  const [preferredSkills, setPreferredSkills] = useState([]);
  const [preferredGender, setPreferredGender] = useState("Male");

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
        let userData = {
          email: email,
          password: password,
          full_name: fullname,
          bio: bio,
          profile_picture_url: profilePictureUrl, // TODO: Get gravator image
          dob: dob,
          gender: gender,
          github_username: githubUsername,
          linkedin_username: linkedinUsername,
          skills: skills,
          country: country,
          hobbies: hobbies,
          preferred_buddy_type: preferredBuddyType,
          preferred_skills: preferredSkills,
          preferred_gender: preferredGender,
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
      <h1>Sign Up</h1>

      <Form onSubmit={submitHandler}>
        <Form.Group className="my-3" controlId="email">
          <Form.Label>Email Address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="confirmPassword">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Confirm password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="fullname">
          <Form.Label>Full Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter full name"
            value={fullname}
            onChange={(e) => setFullname(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="bio">
          <Form.Label>Bio</Form.Label>
          <Form.Control
            as="textarea"
            placeholder="Enter bio"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="dob">
          <Form.Label>Date of Birth</Form.Label>
          <Form.Control
            type="date"
            value={dob}
            onChange={(e) => setDob(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="gender">
          <Form.Label>Gender</Form.Label>
          <Form.Select
            aria-label="Gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
          >
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="my-3" controlId="githubUsername">
          <Form.Label>GitHub Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter GitHub username"
            value={githubUsername}
            onChange={(e) => setGithubUsername(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="linkedinUsername">
          <Form.Label>LinkedIn Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter LinkedIn username"
            value={linkedinUsername}
            onChange={(e) => setLinkedinUsername(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="skills">
          <Form.Label>Skills</Form.Label>
          <PillInputList list={skills} setList={setSkills} />
        </Form.Group>

        <Form.Group className="my-3" controlId="country">
          <Form.Label>Country</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter country"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group className="my-3" controlId="hobbies">
          <Form.Label>Hobbies</Form.Label>
          <PillInputList list={hobbies} setList={setHobbies} />
        </Form.Group>

        <h3 style={{ marginTop: "50px", marginBottom: "20px" }}>
          Buddy Preferences
        </h3>

        <Form.Group className="my-3" controlId="preferredBuddyType">
          <Form.Label>Preferred Buddy Type</Form.Label>
          <Form.Select
            aria-label="Preferred Buddy Type"
            value={preferredBuddyType}
            onChange={(e) => setPreferredBuddyType(e.target.value)}
          >
            <option value="Buddy">Buddy</option>
            <option value="Mentor">Mentor</option>
            <option value="Mentee">Mentee</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="my-3" controlId="preferredSkills">
          <Form.Label>Preferred Skills</Form.Label>
          <PillInputList list={preferredSkills} setList={setPreferredSkills} />
        </Form.Group>

        <Form.Group className="my-3" controlId="preferredGender">
          <Form.Label>Preferred Gender</Form.Label>
          <Form.Select
            aria-label="Preferred Gender"
            value={preferredGender}
            onChange={(e) => setPreferredGender(e.target.value)}
          >
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Any">Any</option>
          </Form.Select>
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
