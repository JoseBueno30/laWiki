
import React, { useContext, useEffect, useState } from 'react';
import {Button, Flex, Grid, Select, Spin} from "antd";
import { EditOutlined, ReloadOutlined} from '@ant-design/icons';
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
import { useTranslation } from 'react-i18next';
import JsxParser from 'react-jsx-parser';

const {useBreakpoint} = Grid

const MapView = null

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
  const {t} = useTranslation()

  const screen = useBreakpoint()
  const [loading, setLoading] = useState(true)
  const [articleVersion, setArticleVersion] = useState(null)
  const [versions, setVersions] = useState([])
  const [comments, setComments] = useState({comments: []})
  const [ratings, setRatings] = useState({average: 0, total: 0, ratings: []})
  const [userRating, setUserRating] = useState({rating_object: null, enabled: false})

  const fetchArticleRatings = async () =>{
    const ratings_response = await RatingService().getArticleRatings(articleVersion.article_id)

    setRatings({average: ratings_response.average, total: ratings_response.total, 
      ratings : [ratings_response.five_count, ratings_response.four_count, 
        ratings_response.three_count, ratings_response.two_count, ratings_response.one_count]})
  }

  const fetchArticleComments = async () =>{
    const comments_response = await CommentService().getArticleComments(articleVersion.article_id, 0, 3,'recent', null)
    setComments(comments_response)
  }

  useEffect(() =>{
    const fetchArticleVersion = async () =>{
      // AÑADIR PROP DE ARTICULO -> SI ES NULO BUSCAR CON LA URL Y SIN LENGUAJE
      console.log("WIKI", wiki)
      const articleName = window.location.toString().split("/").pop().replaceAll("_", " ")
      const version_response = await ArticleService().getArticleVersionByName(wiki.wiki_info.id, articleName, locale) 
      setArticleVersion(version_response)
    }
    if (wiki) fetchArticleVersion()
  }, [wiki])

  const fetchVersions = async () =>{
    const versions_response = await ArticleService().getArticleVersionsByArticleID(articleVersion.article_id)
    setVersions(versions_response.article_versions)
  }

  useEffect(() =>{

    const fetchUserRating = async () =>{
      const userRating_response = await RatingService().getUserRatingInArticle(user.id, articleVersion.article_id);
            
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

  useEffect(() =>{
    if(articleVersion){
      changeURL()
    }
  }, [locale])
  
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

  const loadVersion = async (versionId, _) =>{
    const version_response = await ArticleService().getArticleVersionByID(versionId, locale)
    setArticleVersion(version_response)
  }

  const updateRating = async (newRatingValue) =>{
    let rating_response
    // console.log("NUEVO RATING", newRatingValue)
    if(newRatingValue == 0){
      rating_response = await RatingService().deleteRating(userRating.rating_object.id)
      setUserRating({rating_object: null, enabled: false})
    }else if(userRating.rating_object != null){
      rating_response = await RatingService().updateArticleRating(articleVersion.article_id, user.id, newRatingValue)
      setUserRating({rating_object: rating_response, enabled: true})
    }else{
      rating_response = await RatingService().createArticleRating(articleVersion.article_id, user.id, newRatingValue)
      setUserRating({rating_object: rating_response, enabled: true})
    }
    fetchArticleRatings()
  }

  const uploadComment = async (text) =>{
    await CommentService().postComment(articleVersion.article_id, user.id, text)
    fetchArticleComments()
  }

  const controlCommentsPaginationAndFilters = async (newOffset, order,creation_date) =>{

    const comments_response = await CommentService().getArticleComments(articleVersion.article_id, newOffset, 3, order,creation_date)
    setComments(comments_response)
  }

  const changeURL = () =>{
    const newPart = articleVersion.title[locale];
    const sanitizedNewPart = newPart.replace(/ /g, "_");

    const urlObj = new URL(window.location);
    const pathParts = urlObj.pathname.split("/");
    pathParts[pathParts.length - 1] = sanitizedNewPart;
    urlObj.pathname = pathParts.join("/");

    const newUrl = urlObj.toString();

    // Reload with new URL
    window.location = newUrl;
  }

  const restoreArticleVersion = async () =>{
    const restore_response = await ArticleService().restoreArticleVersion(articleVersion.article_id, articleVersion.id)
    // fetchVersions()  
    changeURL()
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
                    
          <Select title='Seleccionar version' options={formatVersions()} defaultValue={versions[0].id} onChange={loadVersion}></Select> 
          {articleVersion.id == versions[0].id ? 
            <Button title='Edit' icon={<EditOutlined />} iconPosition='start' type='secondary' color='default' variant='outlined'>
              {t('article.edit-article-button')}
            </Button >
            :
            <Button title='Restore' icon={<ReloadOutlined />} iconPosition='start' type='secondary' color='default' variant='outlined' onClick={restoreArticleVersion}>
            {"Restore"}
            </Button>
          }
          
        </Flex>
        
      </Flex>
      <div className='article-body-container'>
        <JsxParser 
        components={{MapView}}
        jsx={articleVersion.body}/>
      </div>
      <Flex className={screen.sm ? '' : 'reversed'} style={{padding: "10px"}} vertical={screen.sm ? false : true} align={screen.sm ? "start" : "center"}>
        <CommentList uploadFunc={uploadComment} commentsObject={comments} user={user} fetchFunc={controlCommentsPaginationAndFilters}></CommentList>  

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
