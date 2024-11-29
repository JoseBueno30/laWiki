
import React, {useEffect, useState} from 'react';
import './articles-search-result-page.css';
import { Flex, Row, Col, Button } from 'antd';
import { useSearchParams, useNavigate } from "react-router-dom";
import ArticleList from '../../components/article-list/article-list';
import axios from "axios";

const articleList = [
  {
    id: "673e4ff8eb2c93347976b0df",
    title: {
      en: "Parkway Drive",
      es: "Parkway Drive",
      fr: "Parkway Drive"
    },
    author: {
      name: "EdgyBoy",
      image: "itachi.png",
      id: "672901e41a1c2dc79c930ded"
    },
    tags: [
      {
        tag: {
          en: "Tag 3",
          es: "Tag 3",
          fr: "Tag 3"
        },
        id: "67310684be72ea3d639689b2"
      }
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
          fr: "Parkway Drive"
        },
        author: {
          name: "EdgyBoy",
          image: "itachi.png",
          id: "672901e41a1c2dc79c930ded"
        },
        lan: "es",
        translate_title: false,
        modification_date: "2024-11-20T22:09:13.574Z",
        id:  "673e4ff9eb2c93347976b0e0"
      }
    ]
  },
  {
    id: "673e4ff8eb2c93347976b0df",
    title: {
      en: "ARTICULO 2",
      es: "AR \n  TICULOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
      fr: "Parkway Drive"
    },
    author: {
      name: "ADRIDUTY",
      image: "itachi.png",
      id: "672901e41a1c2dc79c930ded"
    },
    tags: [
      {
        tag: {
          en: "Tag 3",
          es: "Tag 3",
          fr: "Tag 3"
        },
        id: "67310684be72ea3d639689b2"
      }
    ],
    wiki_id: "672c8721ba3ae42bd5985361",
    lan: "es",
    translate_title: false,
    creation_date: "2024-11-20",
    rating: 0.75,
    versions: [
      {
        title: {
          en: "Parkway Drive",
          es: "Parkway Drive",
          fr: "Parkway Drive"
        },
        author: {
          name: "EdgyBoy",
          image: "itachi.png",
          id: "672901e41a1c2dc79c930ded"
        },
        lan: "es",
        translate_title: false,
        modification_date: "2024-11-20T22:09:13.574Z",
        id:  "673e4ff9eb2c93347976b0e0"
      }
    ]
  },
]

const wiki_id = "672c8721ba3ae42bd5985361"

const ArticlesSearchResultPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [articles, setArticles] = useState([]);

  // TODO: In order to search in a given wiki, should the gateway provide an endpoint to search having only the wiki name? or should the front handle this

  const searchArticles = async () => {
    setLoading(true);
    try{
      var params = {
        wiki_id: wiki_id,
        name: searchParams.get("name") || "",
        tags: searchParams.getAll("tags"),
        offset: 0,
        limit: 10,
        order: searchParams.get("order") || "",
        creation_date: searchParams.get("creation_date") || "",
        author_name: searchParams.get("author_name") || "",
        editor_name: searchParams.get("editor_name") || "",
        lan: "es",
      }

      params = Object.fromEntries(
        Object.entries(params).filter(([_, value]) => value && value.length !== 0)
      );

      const response = await axios.get("http://localhost:3000/v1/articles",{params:params})  

      setArticles(response.data.articles)

    } catch (err){
      console.log(err);
    }finally{
      setLoading(false);
    }
  }

  useEffect(() => {
    setLoading(true);
    searchArticles();
  }, [wiki_id, searchParams])


  return (
    <Flex vertical align="center" style={{minWidth:400}}>
      <h2 className='article-search-results-title'>Search results for: (article_name)</h2>
      <h3 className='article-search-results-info'>Total: (X) | Filters: (used_filters)</h3>
      <ArticleList articleList={articles}/>
      <Row align="middle" justify="space-around" style={{ width:"80%", marginTop:20}}>
        <Col>
          <Button type="primary">Previous</Button>
        </Col>
        <Col>
          Page Nº
        </Col>
        <Col>
          <Button type="primary">Next</Button>
        </Col>
      </Row>
    </Flex>
  );
};

export default ArticlesSearchResultPage;
