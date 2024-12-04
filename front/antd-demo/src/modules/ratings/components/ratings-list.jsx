import { Flex, Rate, Space, Typography, Progress } from "antd";
const { Text } = Typography;
import Title from "antd/es/typography/Title";
import { useTranslation } from "react-i18next";

// Average rating and the ratings list
// It suposses that the ratings are from 1 to 5 and that the
// ratings are stored in an array of objects with the key "value"

// avg_rating : Average rating of the article
// total_ratings : Total count of ratings
// ratings : Array of the total count of ratings for each value
const RatingsList = ({ avg_rating, total_ratings, ratings }) => {
  const { t } = useTranslation();
  return (
    <Flex vertical >
      <Title level={4}>{t('article.global-rating-header')}</Title>
      <Space align="center">
        <Rate disabled value={avg_rating} />
        <span>{t('article.global-rating-value', {value: avg_rating})}</span>
      </Space>
      <Text type="secondary">{t('article.global-rating-count', {count:total_ratings})}</Text>
      <Flex vertical gap="small" style={{ marginTop: "10px" }}>
        {ratings.map((value_count, index) => {
          let i = 5 - index;

          let percent = Math.round((value_count / total_ratings) * 100);
          return (
            <Flex key={i} vertical>
              <Text strong>{t('article.num-stars', {count: i})}</Text>
              <Flex align="start" gap="small">
                <Progress
                  percent={percent}
                  size={[, 15]}
                  strokeColor="#fadb14"
                  showInfo={false}
                />
                <Flex justify="center" align="center">
                  <Text style={{width:"40px", textAlign:"end"}}>{percent ? percent : 0}%</Text>
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
