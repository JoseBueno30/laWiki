import { useContext } from "react";
import APIGateway from "../../../interceptor/interceptor";
import { SettingsContext } from "../../../context/settings-context";

const WikiService = () => {
  const getWiki = async (wiki_name, locale) => {
    try {
      const params = new URLSearchParams({ lang: locale });
      const url = `/v1/wikis/${wiki_name}?${params.toString()}`;

      const response = await APIGateway.get(url);
      return response;
    } catch (error) {
      console.error("WikiService.getWiki:", error);
      return Promise.reject(error);
    }
  };

  const getRatedWikis = async () => {
    try {
      const response = await APIGateway.get("/wikis");
      return response;
    } catch (error) {
      console.error("WikiService.getRatedWikis:", error);
      return Promise.reject(error);
    }
  };

  const createWikiTag = async (wikiId, tag, lang) => {
    try {
      const url = `/v1/tags/wikis/${wikiId}`;
      const payload = {
        tag: tag,
        translation: true,
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
      const url = `/v1/tags/${tagId}`;
      const response = await APIGateway.delete(url);
      return response;
    } catch (error) {
      console.error("WikiService.deleteWikiTag:", error);
      return Promise.reject(error);
    }
  };

  const createWiki = async (data) => {
    try {
      const response = await APIGateway.post("/v1/wikis", data);
      return response;
    } catch (error) {
      console.error("WikiService.createWiki:", error);
      return Promise.reject(error);
    }
  };

  const updateWiki = async (wikiId, data) => {
    try {
      const url = `/v1/wikis/${wikiId}`;
      const response = await APIGateway.put(url, data);
      return response;
    } catch (error) {
      console.error("WikiService.updateWiki:", error);
      return Promise.reject(error);
    }
  };

  const deleteWiki = async (wikiId) => {
    try {
      const url = `/v1/wikis/${wikiId}`;
      const response = await APIGateway.delete(url);
      return response;
    } catch (error) {
      console.error("WikiService.deleteWiki:", error);
      return Promise.reject(error);
    }
  };

  return {
    getWiki,
    getRatedWikis,
    createWikiTag,
    deleteWikiTag,
    updateWiki,
    deleteWiki,
    createWiki
  };
};

export default WikiService;
