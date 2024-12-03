
import React from 'react';
import { Card, Rate, Image } from 'antd';
import './wiki-card-item.css';
import { useNavigate } from 'react-router-dom';

const { Meta } = Card;

const WikiCardItem = ({wiki}) => {
  const navigate = useNavigate();
  const navigateToWiki = () => {
    let newTitle = wiki.name.replace(/\s+/g, '_');
    navigate("/wikis/" + newTitle);
  };
  return (
    <>
        <Card hoverable style={{ width: 360 }} onClick={() => navigateToWiki()}>
          <div className='wiki-image-container'>
            <Image preview={false} className='wiki-image' alt={wiki.name} src={wiki.image ?? ""} height={200} width={"auto"} />
          </div>
          <Meta title={wiki.name} description={wiki.description} />
          <div className='rating-container'>
            {wiki.rating}
            <Rate style={{ marginLeft: 10}} disabled allowHalf value={wiki.rating} />
          </div>
        </Card>
    </>
  );
};

export default WikiCardItem;
