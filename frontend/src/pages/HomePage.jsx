import { useEffect, useState } from "react";
import { Button, Card, Col, Container, Row } from "react-bootstrap";
import { Loader } from "../components";

const HomePage = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/users/me/matches/", {
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
    <Container>
      <Row xs={2} md={4} className="g-4">
        {data ? (
          data.map((match, index) => (
            <Col key={index}>
              <Card>
                <Card.Img variant="top" src={match.profile_pic_url} />
                <Card.Body>
                  <Card.Title>{match.full_name}</Card.Title>
                  <Card.Text>{match.bio}</Card.Text>
                  <Button
                    variant="primary"
                    href={`https://www.linkedin.com/in/${match.linkedin_username}/`}
                    target="_blank"
                  >
                    Connect on LinkedIn
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
