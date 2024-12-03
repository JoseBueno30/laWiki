import { Flex, Space, Rate } from "antd";
import Title from "antd/es/typography/Title";
import RatingsList from "./ratings-list";
import { useState } from "react";

const RatingsSection = () => {

    const [rating, setRating] = useState(0);
    const ratings = [5,10,0,20,0];
    const total_ratings = 35;
    const avg_rating = 4.75;

    const updateRating = (value) => {
        setRating(value);
    };

    return (
        <Flex vertical style={{ maxWidth: "300px", margin: "1em" }}>
            <Space direction="vertical" size='small'>
                <Title level={4}>Your rating</Title>
                <Rate value={rating} onChange={updateRating}/>
            </Space>
            <RatingsList avg_rating={avg_rating} total_ratings={total_ratings} ratings={ratings} />
        </Flex>
    );
}

export default RatingsSection;