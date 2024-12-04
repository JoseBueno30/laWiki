import { useContext } from "react";
import APIGateway from "../../../interceptor/interceptor";
import { SettingsContext } from "../../../context/settings-context";

const WikiService = () => {
  const getWiki = async (wiki_name) => {
    try {
      const params = new URLSearchParams({ lang: localStorage.getItem("locale") });
      const url = `/v1/wikis/${wiki_name}?${params.toString()}`;

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
        const url = `/v1/wikis/?${params.toString()}`;
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

  return {
    getWiki,
    getRatedWikis,
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
