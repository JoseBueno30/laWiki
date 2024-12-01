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

const generateDateRange = (startDate, endDate) => (
  startDate && endDate ? `${startDate}-${endDate}` : startDate ? `${startDate}` : endDate ? `${endDate}` : ""
)

const isQueryValid = (query) => {
  return query.trim().length > 0;
};

// Aqui seguramente se pase la informacion de la wiki, como el nombre, id y tags.
const WikiHeader = ({wiki_name,wiki}) => {
  const [showSearchHeader, setSearchHeader] = useState(true);

  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState({
    order: "recent",
    tags: [],
    author: "",
    editor: "",
    startDate: "2024/01/01",
  });

  const {locale} = useContext(SettingsContext);
  const { t } = useTranslation('header');
  const navigate = useNavigate();

  const toggleSearchHeader = () => {
    setSearchHeader(!showSearchHeader);
  };

  const searchHandler = () => {
    if (!isQueryValid(searchQuery)) {
      console.log("Invalid search query");
      return;
    }

    const searchParams = new URLSearchParams();
    searchParams.append("name", searchQuery);
    searchParams.append("order", filters.order);
    searchParams.append("tags", filters.tags.join(","));
    isQueryValid(filters.author) ?  searchParams.append("author_name", filters.author) : null;
    isQueryValid(filters.editor) ?  searchParams.append("editor_name", filters.editor) : null;
    searchParams.append("creation_date", generateDateRange(filters.startDate, filters.endDate));

    console.log(generateDateRange(filters.startDate, filters.endDate));

    const searchUrl = `/wikis/${wiki_name}/search?${searchParams.toString()}`;
    navigate(searchUrl)
  }

  // Hay que definir una funcion de searchFunction(), la cual se pasará a los componentes de input
  // Esa funcion hará uso de un useNavigate de React router, el cual tiene el mismo efecto
  // que el <Link to>. Esto facilita mucho el añadido de parametros a la URL.

  return (
    <>
      {showSearchHeader ? (
        <>
          <div className="header-title-container">
            <Link to="/" reloadDocument>
              <Title level={3} className="header-title wiki-title">
                LaWiki
              </Title>
            </Link>
            {/* Depende de la información que le venga de la ruta */}

            <Title level={3} className="header-title">
              /
            </Title>
            <Link to={`/wikis/${wiki_name}`} reloadDocument>
              <Title level={3} className="header-title wiki-title">
                {wiki.name[locale]}
              </Title>     
            </Link>
          </div>

          <div className="header-tools">
            <SearchInput
              searchPlaceholder={t('article-search-placeholder')}
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
            <CreateButton text={t('new-article')} />
            <Badge count={9} size="large">
              <div
                className="icon-container"
                onClick={NotificationsClickHandler}
              >
                <BellOutlined style={{ fontSize: "24px" }} />
              </div>
            </Badge>
            <Popover
              content={<UserProfilePopover />}
              trigger="click"
              placement="bottomRight"
              overlayStyle={{ width: 270 }}
            >
              <Flex className="icon-container">
                <Avatar size="large" icon={<UserOutlined />} />
              </Flex>
            </Popover>
          </div>
        </>
      ) : (
        <CompactSearchInput
          searchPlaceholder={t('article-search-placeholder')}
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
