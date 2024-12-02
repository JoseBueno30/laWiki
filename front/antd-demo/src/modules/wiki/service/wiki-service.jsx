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

  return {
    getWiki,
    getRatedWikis,
  };
};

export default WikiService;
