
import React, { useContext, useEffect, useState } from 'react';
import {Avatar, Button, Flex, Grid, Select, Spin,Typography} from "antd";
import { EditOutlined } from '@ant-design/icons';
import CommentList from '../../../comments/components/comment-list/comment-list';
import RatingsSection from '../../components/ratings-section';
import UserAvatar from '../../../wiki/components/avatar/user-avatar';
import './article-page.css';
import Title from 'antd/es/typography/Title';
import ArticleService from '../../service/article-service';
import { WikiContext } from '../../../../context/wiki-context';
import SettingsContext from '../../../../context/settings-context';

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
  const user = {
    name: "Adriduty",
    image: "https://i1.sndcdn.com/artworks-ynfN32NPS8zDyraR-PHw2zQ-t500x500.jpg",
    id: "1"
  }

const ArticlePage = () => {

  const {wiki} = useContext(WikiContext)
  const {locale} = useContext(SettingsContext)

  const screen = useBreakpoint()
  const [loading, setLoading] = useState(true)
  const [articleVersion, setArticleVersion] = useState(null)

  useEffect(() =>{
    const fetchArticleVersion = async () =>{
      // console.log("URL:", window.location.toString().split("/"))
      const articleName = window.location.toString().split("/").pop().replaceAll("%20", " ")
      const response = await ArticleService().getArticleVersionByName("672c8721ba3ae42bd5985361", articleName, locale) 
      setArticleVersion(response)
    }
    fetchArticleVersion()
    console.log("adios")
  }, [])

  useEffect(() =>{
    if (articleVersion){
      setLoading(false)
    }
    console.log("hola")
  }, [articleVersion])
  
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

  const parseBodyToHTML = () =>{
    var el = document.createElement( 'section' );
    el.innerHTML = articleVersion.body
    console.log("HTML" ,el)
  }

  return (
    loading ?
    <Spin className='loading-article-page' size='large'></Spin>
    :
    (<section className='article-page'>
      <Flex align='center' justify='space-between'>
        <Title>
          {articleVersion.title.es}
        </Title>
        <Flex gap={screen.md ? "3dvw" : 10} vertical={screen.md ? false : true} align='center'  style={screen.md ? {paddingTop: 25}:{paddingTop: 15}}>
          <Button color='default' variant='text'>
            <UserAvatar image={article.author.image} username={article.author.name}></UserAvatar>
          </Button>
          
          {/* Parsear versiones a opciones*/}
          <Select title='Seleccionar version' options={formatVersions(article.versions)} defaultValue={article.versions[0].id}></Select> 
          <Button title='Editar' icon={<EditOutlined />} iconPosition='start' type='secondary' color='default' variant='outlined'>
            "Editar"
          </Button>
        </Flex>
        
      </Flex>
      <div className='article-body-container'>
        <section dangerouslySetInnerHTML={{__html: articleVersion.body}}></section>
      </div>
      <Flex className={screen.sm ? '' : 'reversed'} style={{padding: "10px"}} vertical={screen.sm ? false : true} align={screen.sm ? "start" : "center"}>
        <CommentList commentList={[]} user={user}></CommentList>     
        <RatingsSection></RatingsSection> 
      </Flex>

    </section>)
  );
};

export default ArticlePage;
