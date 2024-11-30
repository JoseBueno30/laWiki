
import React, { useEffect, useState } from 'react';
import {Avatar, Button, Flex, Grid, Select,Typography} from "antd";
import { EditOutlined } from '@ant-design/icons';
import './article-page.css';
import Title from 'antd/es/typography/Title';
const {useBreakpoint} = Grid

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
      image: "https://i.imgur.com/zglEouG.jpeg",
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
  const screen = useBreakpoint()
  
  const formatVersions = () => {
    let simplifiedVersions = [] 

    article.versions.forEach(element => {
      const newVersion = {
        value: element.id,
        label: screen.md ? 
          <span>{element.modification_date.substring(0,10) + " " + element.title[element.lan]}</span> 
          :
          <span>{element.modification_date.substring(0,10)}</span> 
      }
      simplifiedVersions.push(newVersion)
    });
    
    return simplifiedVersions;
  }

  console.log("titulo: " + article.title.es)
  return (
    <section className='article-page'>
      <Flex align='center' justify='space-between'>
        <Title>
          {article.title.es}
        </Title>
        <Flex gap={screen.md ? 30 : 10} vertical={screen.md ? false : true} align='center'  style={screen.md ? {paddingTop: 25}:{paddingTop: 15}}>
          <Button color='default' variant='text'>
            <Flex align='center' gap={5}>
              {/* Ajustar Texto de author */}
              <Avatar className='comment-avatar' src={article.author.image} alt={article.author.name} />
              {<Text className='article-prop-text'>{article.author.name}</Text>}
            </Flex>
          </Button>
          
          {/* Parsear versiones a opciones*/}
          <Select title='Seleccionar version' options={formatVersions(article.versions)} defaultValue={article.versions[0].id}></Select> 
          <Button title='Editar' icon={<EditOutlined />} iconPosition='start' type='secondary' color='default' variant='outlined'>
            {screen.md ? "Editar" : "Editar"}
          </Button>
        </Flex>
        
      </Flex>
      <div className='article-body-container'>
        ...
      </div>

    </section>
  );
};

export default ArticlePage;
