import { Flex,Grid, Space, Rate } from "antd";
import Title from "antd/es/typography/Title";
import RatingsList from "./ratings-list";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

const{useBreakpoint} = Grid

const RatingsSection = ({ratings, total_ratings, avg_rating, updateRatingFunc, user_value}) => {
    const screen = useBreakpoint()
    const { t } = useTranslation();
    const [rating, setRating] = useState(user_value);
    
    // const ratings = [5,10,0,20,0];
    // const total_ratings = 35;
    // const avg_rating = 4.75;
    
    useEffect(() =>{
        setRating(user_value)
    })

    const updateRating = (value) => {
        setRating(value);
        updateRatingFunc(value)
    };

    return (
        
        <Flex vertical style={{ maxWidth: "300px", minWidth: (screen.md ? "26dvw": (screen.sm ? "200px" : "100%")), margin: "1em" }}>
            <Space direction="vertical" size='small'>
                <Title level={4}>{t('article.user-rating-header')}</Title>
                {/* {console.log("USERRATING ?",rating, "vs",user_value)} */}
                <Rate value={rating} onChange={updateRating}/>
            </Space>
            <RatingsList avg_rating={avg_rating} total_ratings={total_ratings} ratings={ratings} />
        </Flex>
    );
}

export default RatingsSection;