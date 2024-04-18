import { useEffect, useState } from "react";
import { Button, Card, Col, Container, Row } from "react-bootstrap";
import { FaGithub, FaLinkedin } from "react-icons/fa";
import shave from "shave";
import { Loader } from "../components";

const HomePage = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    shave(".text-truncate-2", 50); // 50 is the maximum height in pixels
  }, [data]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/users/me/recommendations/", {
          credentials: "include", // include cookies in the request
        });
        const data = await response.json();
        console.log(data);
        setData(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return (
    <Container className="px-5 py-5">
      <p className="text-center mb-4">
        Here are some coding buddy recommendations based on your profile.
      </p>
      <Row
        style={{ paddingLeft: "50px", paddingRight: "50px" }}
        xs={1}
        md={3}
        className="g-4"
      >
        {data ? (
          data.map((match, index) => (
            <Col key={index}>
              <Card className="h-100 text-center">
                <Card.Img variant="top" src={match.profile_image} />
                <Card.Body className="d-flex flex-column">
                  <Card.Title className="font-weight-bold my-3">
                    {match.full_name}
                  </Card.Title>
                  <Card.Text className="text-truncate-2">{match.bio}</Card.Text>
                  <Button
                    variant="warning"
                    href={`${match.github_profile}`}
                    target="_blank"
                    className="mt-auto mr-2"
                  >
                    Check out <FaGithub /> GitHub
                  </Button>
                  <Button
                    variant="primary"
                    href={`${match.linkedin_profile}`}
                    target="_blank"
                    className="mt-2"
                  >
                    Connect on <FaLinkedin /> LinkedIn
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          ))
        ) : (
          <Loader />
        )}
      </Row>
    </Container>
  );
};

export default HomePage;
