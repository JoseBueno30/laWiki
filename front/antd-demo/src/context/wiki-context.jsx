import { useEffect, createContext, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { useContext } from "react";
import { SettingsContext } from "./settings-context";
import WikiService from "../modules/wiki/service/wiki-service";

const { getWiki } = WikiService();

export const WikiContext = createContext();

const convertUnderscoreToSpace = (str) => {
  return str.replace(/_/g, " ");
};

export const WikiProvider = ({ children }) => {
  //Inicialmente no tiene nada
  const [wiki, setWiki] = useState({ wiki_name: "", wiki_info: null });
  const { wiki_name } = useParams();
  const { locale } = useContext(SettingsContext);

  const fetchWiki = async () => {
    try {
      const formattedWikiName = convertUnderscoreToSpace(wiki_name);
      const wikiData = await getWiki(formattedWikiName, locale);

      console.log(wikiData);
      setWiki({ wiki_name: wiki_name, wiki_info: wikiData });
      
    } catch (error) {
      console.error("WikiProvider:", error);
    }
  };

  useEffect(() => {
    if (!wiki_name) {
      // Si no hay wiki_name, resetea el estado
      setWiki({ wiki_name: "", wiki_info: null });
    } else if (wiki_name !== wiki.wiki_name) {
      // Si el wiki_name es diferente al actual, busca la nueva
      // wiki y actualiza el estado
      fetchWiki();
    }
  }, [wiki_name]);

  return (
    <WikiContext.Provider value={{wiki}}>
        {children}
    </WikiContext.Provider>
  );
};
