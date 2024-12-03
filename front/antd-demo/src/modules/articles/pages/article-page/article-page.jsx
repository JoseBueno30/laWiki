
import React, { useContext, useEffect, useState } from 'react';
import {Button, Flex, Grid, Select, Spin} from "antd";
import { EditOutlined } from '@ant-design/icons';
import CommentList from '../../../comments/components/comment-list/comment-list';
import RatingsSection from '../../../ratings/components/ratings-section';
import UserAvatar from '../../../wiki/components/avatar/user-avatar';
import './article-page.css';
import Title from 'antd/es/typography/Title';
import ArticleService from '../../service/article-service';
import CommentService from '../../../comments/service/comment-service';
import { WikiContext } from '../../../../context/wiki-context';
import SettingsContext from '../../../../context/settings-context';
import RatingService from '../../../ratings/service/rating-service';

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
    id: "672272c65150a9cd3f46599e"
  }

const ArticlePage = () => {

  const {wiki} = useContext(WikiContext)
  const {locale} = useContext(SettingsContext)

  const screen = useBreakpoint()
  const [loading, setLoading] = useState(true)
  const [articleVersion, setArticleVersion] = useState(null)
  const [versions, setVersions] = useState([])
  const [comments, setComments] = useState({comments: []})
  const [ratings, setRatings] = useState({average: 0, total: 0, ratings: []})
  const [userRating, setUserRating] = useState({rating_object: null, enabled: false})

  useEffect(() =>{
    const fetchArticleVersion = async () =>{
      // AÑADIR PROP DE ARTICULO -> SI ES NULO BUSCAR CON LA URL Y SIN LENGUAJE
      // console.log("URL:", window.location.toString().split("/"))
      const articleName = window.location.toString().split("/").pop().replaceAll("_", " ")
      const version_response = await ArticleService().getArticleVersionByName(/*"672c8721ba3ae42bd5985361"*/wiki.wiki_info.id, articleName, locale) 
      setArticleVersion(version_response)
    }
    fetchArticleVersion()
  }, [wiki])

  useEffect(() =>{
    const fetchVersions = async () =>{
      const versions_response = await ArticleService().getArticleVersionsByArticleID(articleVersion.article_id)
      setVersions(versions_response.article_versions)
    }

    const fetchArticleComments = async () =>{
      const comments_response = await CommentService().getArticleComments(articleVersion.article_id, 0, 3, null)
      // console.log("COMMENTS", comments_response)
      setComments(comments_response)
    }

    const fetchArticleRatings = async () =>{
      const ratings_response = await RatingService().getArticleRatings(articleVersion.article_id)

      setRatings({average: ratings_response.average, total: ratings_response.total, 
        ratings : [ratings_response.five_count, ratings_response.four_count, 
          ratings_response.three_count, ratings_response.two_count, ratings_response.one_count]})
    }

    const fetchUserRating = async () =>{
      const userRating_response = await RatingService().getUserRatingInArticle(user.id, articleVersion.article_id);
      
      // console.log("RATING_RESPONSE:",userRating_response)
      
      setUserRating({
        rating_object: userRating_response,
        enabled: true
      })
    }

    if(articleVersion){
      fetchVersions()
      fetchArticleComments()
      fetchArticleRatings()
      fetchUserRating()
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

  const updateRating = async (newRatingValue) =>{
    if(userRating.rating_object != null){
      let newRatingObject = userRating.rating_object 
      newRatingObject.value = newRatingValue
      const rating_response = await RatingService().updateArticleRating(articleVersion.article_id, newRatingObject)
      setUserRating({rating_object: rating_response, enabled: true})
    }else{
      const rating_response = await RatingService().createArticleRating(articleVersion.article_id, user.id, newRatingValue)
      setUserRating({rating_object: rating_response, enabled: true})
    }
  }

  const controlCommentsPaginationAndFilters = async (newOffset, order,creation_date) =>{

    const comments_response = await CommentService().getArticleComments(articleVersion.article_id, newOffset, 3, order,null)
    console.log("CONTROLCOMMENTS", comments_response)
    setComments(comments_response)
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
          
           {/*console.log(versions)*/}
          
          <Select title='Seleccionar version' options={formatVersions()} defaultValue={versions[0].id}></Select> 
          <Button title='Editar' icon={<EditOutlined />} iconPosition='start' type='secondary' color='default' variant='outlined'>
            Editar
          </Button>
        </Flex>
        
      </Flex>
      <div className='article-body-container'>
        // PONER JPARSER
        <section dangerouslySetInnerHTML={{__html: articleVersion.body}}></section>
      </div>
      <Flex className={screen.sm ? '' : 'reversed'} style={{padding: "10px"}} vertical={screen.sm ? false : true} align={screen.sm ? "start" : "center"}>
        <CommentList commentsObject={comments} user={user} fetchFunc={controlCommentsPaginationAndFilters}></CommentList>  

        <RatingsSection ratings={ratings.ratings} avg_rating={ratings.average} 
          total_ratings={ratings.total} 
          updateRatingFunc={updateRating} 
          user_value={userRating.rating_object ? userRating.rating_object.value : 0}>
        </RatingsSection> 
      </Flex>
    </section>)
  );
};

export default ArticlePage;
