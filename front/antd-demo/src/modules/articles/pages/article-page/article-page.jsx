
import React from 'react';
import {Avatar, Button, Flex, Select,Typography} from "antd";
import './article-page.css';

const {Text, _} = Typography

const article =
  {
    id: "673e4ff8eb2c93347976b0df",
    title: {
      en: "Parkway Drive",
      es: "Parkway Drive",
      fr: "Parkway Drive",
    },
    author: {
      name: "EdgyBoy",
      image: "itachi.png",
      id: "672901e41a1c2dc79c930ded",
    },
    tags: [
      {
        tag: {
          en: "Tag 3",
          es: "Tag 3",
          fr: "Tag 3",
        },
        id: "67310684be72ea3d639689b2",
      },
    ],
    wiki_id: "672c8721ba3ae42bd5985361",
    lan: "es",
    translate_title: false,
    creation_date: "2024-11-20",
    rating: 4.75,
    versions: [
      {
        title: {
          en: "Parkway Drive",
          es: "Parkway Drive",
          fr: "Parkway Drive",
        },
        author: {
          name: "EdgyBoy",
          image: "itachi.png",
          id: "672901e41a1c2dc79c930ded",
        },
        lan: "es",
        translate_title: false,
        modification_date: "2024-11-20T22:09:13.574Z",
        id: "673e4ff9eb2c93347976b0e0",
      },
    ],
  };

  const ArticlePage = ({/*article*/}) => {
  console.log("titulo: " + article.title.es)
  return (
    <section className='article-page'>
      <Flex align='center' justify='space-between'>
        <h1>
          {article.title.es}
        </h1>
        <Flex gap={"middle"}>
          <Flex >
            {/* Ajustar Texto de author */}
            <Avatar className='comment-avatar' src={article.author.image} alt={article.author.name} />
            <Text>El coleccionista</Text>
          </Flex>
          
          {/* Parsear versiones a opciones*/}
          <Select options={article.versions}></Select> 
          <Button type='secondary'>Editar</Button>
        </Flex>
        
      </Flex>
      <div className='article-body-container'>
        ...
      </div>

    </section>
  );
};

export default ArticlePage;
