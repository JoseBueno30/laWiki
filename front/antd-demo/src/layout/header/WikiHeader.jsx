import "./PageHeader.css";
import { Flex, Input, Button, Badge, Avatar, Popover, Grid } from "antd";
import {
  ControlOutlined,
  PlusOutlined,
  BellOutlined,
  UserOutlined,
} from "@ant-design/icons";
import Title from "antd/es/typography/Title";
import { FilterIcon } from "../../utils/icons";
import { useState, useContext } from "react";
const { useBreakpoint } = Grid;
import { Link, Navigate } from "react-router-dom";

import CreateButton from "./buttons/create-button";
import SearchInput from "./buttons/search-input";
import ArticlesFilterPopover from "./popovers/articles-filter-popover";
import UserProfilePopover from "./popovers/UserProfilePopover";
import CompactSearchInput from "./buttons/compact-search-input";
import SettingsContext from "../../context/settings-context";

import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

const NotificationsClickHandler = () => {
  console.log("Notifications clicked");
};

const generateDateRange = (startDate, endDate) =>
  startDate && endDate
    ? `${startDate}-${endDate}`
    : startDate
    ? `${startDate}`
    : endDate
    ? `${endDate}`
    : "";

const isQueryValid = (query) => {
  return query != null && query.trim().length > 0;
};

// Aqui seguramente se pase la informacion de la wiki, como el nombre, id y tags.
const WikiHeader = ({ wiki_name, wiki }) => {
  const [showSearchHeader, setSearchHeader] = useState(true);

  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState({
    order: "popular",
    tags: [],
    author: "",
    editor: "",
    startDate: "",
  });

  const { locale } = useContext(SettingsContext);
  const { t } = useTranslation();
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));

  const toggleSearchHeader = () => {
    setSearchHeader(!showSearchHeader);
  };

  const searchHandler = () => {
    if (!isQueryValid(searchQuery)) {
      console.log("Invalid search query");
      return;
    }

    const searchParams = new URLSearchParams();
    searchParams.append("name", searchQuery.replaceAll(" ", "_"));
    searchParams.append("order", filters.order);
    if (filters.tags.length > 0)
      searchParams.append("tags", filters.tags.join(","));
    if (isQueryValid(filters.author))
      searchParams.append("author_name", filters.author);
    if (isQueryValid(filters.editor))
      searchParams.append("editor_name", filters.editor);
    if (isQueryValid(filters.startDate))
      searchParams.append(
        "creation_date",
        generateDateRange(filters.startDate, filters.endDate)
      );
    searchParams.append("page", 1);

    console.log(generateDateRange(filters.startDate, filters.endDate));

    const searchUrl = `/wikis/${wiki_name}/search?${searchParams.toString()}`;
    navigate(searchUrl);
  };

  // Hay que definir una funcion de searchFunction(), la cual se pasará a los componentes de input
  // Esa funcion hará uso de un useNavigate de React router, el cual tiene el mismo efecto
  // que el <Link to>. Esto facilita mucho el añadido de parametros a la URL.

  return (
    <>
      {showSearchHeader ? (
        <>
          <div className="header-title-container">
            <Link to="/" >
              <Title level={3} className="header-title wiki-title">
                LaWiki
              </Title>
            </Link>
            {/* Depende de la información que le venga de la ruta */}

            <Title level={3} className="header-title">
              /
            </Title>
            <Link to={`/wikis/${wiki_name}`} >
              <Title level={3} className="header-title wiki-title">
                {wiki.name[locale]}
              </Title>
            </Link>
          </div>

          <div className="header-tools">
            <SearchInput
              searchPlaceholder={t("wikis.article-search-placeholder")}
              toggleHeader={toggleSearchHeader}
              query={searchQuery}
              setQuery={setSearchQuery}
              popover={
                <ArticlesFilterPopover
                  filters={filters}
                  setFilters={setFilters}
                  wikiTags={wiki.tags}
                />
              }
              searchFunction={searchHandler}
            />
            <Link to={`/wikis/${wiki_name}/articles/new`}>
              <CreateButton text={t("wikis.new-article")} />
            </Link>
            
            <Popover
              content={<UserProfilePopover />}
              trigger="click"
              placement="bottomRight"
              overlayStyle={{ width: 270 }}
            >
              <Flex className="icon-container">
                <Avatar size="large" src={user ? user.image: undefined} icon={user ? "":<UserOutlined />} />
              </Flex>
            </Popover>
          </div>
        </>
      ) : (
        <CompactSearchInput
          searchPlaceholder={t("wikis.article-search-placeholder")}
          query={searchQuery}
          setQuery={setSearchQuery}
          toggleHeader={toggleSearchHeader}
          popover={
            <ArticlesFilterPopover
              filters={filters}
              setFilters={setFilters}
              wikiTags={wiki.tags}
            />
          }
          searchFunction={searchHandler}
        />
      )}
    </>
  );
};

export default WikiHeader;
