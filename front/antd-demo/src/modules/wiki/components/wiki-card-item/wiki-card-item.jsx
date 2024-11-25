
import React from 'react';
import { Card, Rate } from 'antd';
import './wiki-card-item.css';

const { Meta } = Card;

const WikiCardItem = ({title, description, rating, image}) => {
  return (
    <>
      <Card hoverable style={{ width: 360 }}>
        <div className='wiki-image-container'>
          <img className='wiki-image' alt={title} src={image} />
        </div>
        <Meta title={title} description={description} />
        <div className='rating-container'>
          {rating}
          <Rate style={{ marginLeft: 10 }} disabled allowHalf value={rating} />
        </div>
      </Card>
    </>
  );
};

export default WikiCardItem;
