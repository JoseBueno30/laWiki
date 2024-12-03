import { Flex, Rate, Space, Typography, Progress } from "antd";
const { Text } = Typography;
import Title from "antd/es/typography/Title";

// Average rating and the ratings list
// It suposses that the ratings are from 1 to 5 and that the
// ratings are stored in an array of objects with the key "value"

// avg_rating : Average rating of the article
// total_ratings : Total count of ratings
// ratings : Array of the total count of ratings for each value
const RatingsList = ({ avg_rating, total_ratings, ratings }) => {
  return (
    <Flex vertical >
      <Title level={4}>Other readers opinion</Title>
      <Space align="center">
        <Rate disabled value={avg_rating} />
        <span>{avg_rating} of 5</span>
      </Space>
      <Text type="secondary">{total_ratings} global ratings</Text>
      <Flex vertical gap="small" style={{ marginTop: "10px" }}>
        {ratings.map((value_count, index) => {
          let i = 5 - index;

          let percent = Math.round((value_count / total_ratings) * 100);
          return (
            <Flex key={i} vertical>
              <Text strong>{i} stars</Text>
              <Flex align="start" gap="small">
                <Progress
                  percent={percent}
                  size={[, 15]}
                  strokeColor="#fadb14"
                  showInfo={false}
                />
                <Flex justify="center" align="center">
                  <Text style={{width:"40px", textAlign:"end"}}>{percent}%</Text>
                </Flex>
              </Flex>
            </Flex>
          );
        })}
      </Flex>
    </Flex>
  );
};

export default RatingsList;
