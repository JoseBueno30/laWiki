import { useContext } from "react";
import APIGateway from "../../../interceptor/interceptor";
import { SettingsContext } from "../../../context/settings-context";

const WikiService = () => {
  const getWiki = async (wiki_name) => {
    try {
      const params = new URLSearchParams({ lang: localStorage.getItem("locale") });
      const url = `/wikis/${wiki_name}?${params.toString()}`;

      const response = await APIGateway.get(url);
      response.rating = parseFloat(response.rating.toFixed(2))
      const exists = await checkImageExists(response.image);
        if (!exists) {
          response.image = "https://via.placeholder.com/360x200.png?text=No+Image+Available";
        }

      return response;
    } catch (error) {
      console.error("WikiService.getWiki:", error);
      return Promise.reject(error);
    }
  };

  const getRatedWikis = async () => {
    try {
        const params = new URLSearchParams({ lang: localStorage.getItem("locale") });
        const url = `/wikis?${params.toString()}`;
        let response = await APIGateway.get(url);
        const wikisWithImages = await Promise.all(
          response.wikis.map(async (wiki) => {
              const exists = await checkImageExists(wiki.image);
              if (!exists) {
                  wiki.image = "https://via.placeholder.com/360x200.png?text=No+Image+Available";
              }
              return wiki;
          })
        );
        response.wikis = wikisWithImages;
        return response;
    } catch (error) {
        console.error("WikiService.getRatedWikis:", error);
        return Promise.reject(error);
    }
  };

  const searchWikisWithPaginationURL = async (paginationURL, locale) => {
    try {
      const url = paginationURL + "&lang=" + locale;
      return await APIGateway.get(url);
    }catch (error) {
      console.error("WikiService.searchWikis:", error);
      return Promise.reject(error);
    }
  }

  const searchWikisWithParams = async (queryParams) => {
    try {
      return await APIGateway.get("/wikis", {
        params: queryParams,
      });
    }catch (error) {
      console.error("WikiService.searchWikis:", error);
      return Promise.reject(error);
    }
  }

  const createWikiTag = async (wikiId, tag, lang, translate) => {
    try {
      const url = `/tags/wikis/${wikiId}`;
      const payload = {
        tag: tag,
        translation: translate,
        lan: lang,
      };
      const response = await APIGateway.post(url, payload);
      return response;
    } catch (error) {
      console.error("WikiService.createWikiTag:", error);
      return Promise.reject(error);
    }
  };

  const deleteWikiTag = async (tagId) => {
    try {
      const url = `/tags/${tagId}`;
      const response = await APIGateway.delete(url);
      return response;
    } catch (error) {
      console.error("WikiService.deleteWikiTag:", error);
      return Promise.reject(error);
    }
  };

  const createWiki = async (data) => {
    try {
      const response = await APIGateway.post("/wikis", data);
      return response;
    } catch (error) {
      console.error("WikiService.createWiki:", error);
      return Promise.reject(error);
    }
  };

  const updateWiki = async (wikiId, data) => {
    try {
      const url = `/wikis/${wikiId}`;
      const response = await APIGateway.put(url, data);
      return response;
    } catch (error) {
      console.error("WikiService.updateWiki:", error);
      return Promise.reject(error);
    }
  };

  const deleteWiki = async (wikiId) => {
    try {
      const url = `/wikis/${wikiId}`;
      const response = await APIGateway.delete(url);
      return response;
    } catch (error) {
      console.error("WikiService.deleteWiki:", error);
      return Promise.reject(error);
    }
  };

  return {
    getWiki,
    searchWikisWithParams,
    searchWikisWithPaginationURL,
    getRatedWikis,
    createWikiTag,
    deleteWikiTag,
    updateWiki,
    deleteWiki,
    createWiki
  };


  function checkImageExists(url) {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => resolve(true);
      img.onerror = () => resolve(false);
      img.src = url;
    });
  }
};

export default WikiService;
