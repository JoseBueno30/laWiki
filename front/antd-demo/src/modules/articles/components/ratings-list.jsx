import { Flex, Rate, Space, Typography, Progress } from "antd";
const { Text } = Typography;
import Title from "antd/es/typography/Title";

// Average rating and the ratings list
// It suposses that the ratings are from 1 to 5 and that the 
// ratings are stored in an array of objects with the key "value"
const RatingsList = ({ avg_rating, ratings }) => {
  const total = ratings.length;
  return (
    <Flex vertical style={{ maxWidth: "300px", margin: "1em" }}>
      <Title level={4}>Other readers opinion</Title>
      <Space align="center">
        <Rate disabled value={avg_rating} />
        <span>{avg_rating} of 5</span>
      </Space>
      <Text type="secondary">{total} global ratings</Text>
      <Flex vertical gap="small" style={{ marginTop: "10px" }}>
        {[5, 4, 3, 2, 1].map((i) => {
          let stars = Math.round(
            (ratings.filter((rating) => rating.value === i).length / total) *
              100
          );
          return (
            <Flex key={i} vertical>
              <Text strong>
                {i} stars
              </Text>
                <Progress percent={stars} size={[, 15]} strokeColor="#fadb14"/>
            </Flex>
          );
        })}
      </Flex>
    </Flex>
  );
};

export default RatingsList;
