
import React, { useContext, useEffect, useState } from 'react';
import {Button, Flex, Grid, Select, Spin} from "antd";
import { EditOutlined } from '@ant-design/icons';
import CommentList from '../../../comments/components/comment-list/comment-list';
import RatingsSection from '../../components/ratings-section';
import UserAvatar from '../../../wiki/components/avatar/user-avatar';
import './article-page.css';
import Title from 'antd/es/typography/Title';
import ArticleService from '../../service/article-service';
import CommentsService from '../../../comments/service/comment-service';
import { WikiContext } from '../../../../context/wiki-context';
import SettingsContext from '../../../../context/settings-context';

const {useBreakpoint} = Grid

const article =
  {
    author:{
      image: "https://i.imgur.com/5CAdhgd.jpeg"
    }
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
  const [versions, setVersions] = useState([])
  const [comments, setComments] = useState({comments: []})

  useEffect(() =>{
    const fetchArticleVersion = async () =>{
      // console.log("URL:", window.location.toString().split("/"))
      const articleName = window.location.toString().split("/").pop().replaceAll("%20", " ")
      const version_response = await ArticleService().getArticleVersionByName("672c8721ba3ae42bd5985361", articleName, locale) 
      setArticleVersion(version_response)
    }

    fetchArticleVersion()
  }, [])

  useEffect(() =>{
    const fetchVersions = async () =>{
      const versions_response = await ArticleService().getArticleVersionsByArticleID(articleVersion.article_id)
      setVersions(versions_response.article_versions)
    }

    const fetchArticleComments = async () =>{
      const comments_response = await CommentsService().getArticleComments(articleVersion.article_id, 0, null)
      console.log("COMMENTS", comments_response)
      setComments(comments_response)
    }

    if(articleVersion){
      fetchVersions()
      fetchArticleComments()
    } 
  }, [articleVersion])

  useEffect(() =>{
    if (articleVersion && versions.length > 0 ){
      setLoading(false)
    }
    
  }, [articleVersion, versions])
  
  const formatVersions = () => {
    let simplifiedVersions = [] 

    versions.forEach(element => {
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

  return (
    loading ?
    <Spin className='loading-article-page' size='large'></Spin>
    :
    (<section className='article-page'>
      <Flex align='center' justify='space-between'>
        <Title>
          {articleVersion.title[locale]}
        </Title>
        <Flex gap={screen.md ? "3dvw" : 10} vertical={screen.md ? false : true} align='center'  style={screen.md ? {paddingTop: 25}:{paddingTop: 15}}>
          <Button color='default' variant='text'>
            <UserAvatar image={article.author.image} username={articleVersion.author.name}></UserAvatar>
          </Button>
          
          {console.log(versions)}
          
          <Select title='Seleccionar version' options={formatVersions()} defaultValue={versions[0].id}></Select> 
          <Button title='Editar' icon={<EditOutlined />} iconPosition='start' type='secondary' color='default' variant='outlined'>
            Editar
          </Button>
        </Flex>
        
      </Flex>
      <div className='article-body-container'>
        <section dangerouslySetInnerHTML={{__html: articleVersion.body}}></section>
      </div>
      <Flex className={screen.sm ? '' : 'reversed'} style={{padding: "10px"}} vertical={screen.sm ? false : true} align={screen.sm ? "start" : "center"}>
        <CommentList commentList={comments.comments} user={user}></CommentList>     
        <RatingsSection></RatingsSection> 
      </Flex>

    </section>)
  );
};

export default ArticlePage;
