import "./PageHeader.css";
import { Flex, Badge, Avatar, Popover, Grid } from "antd";
import { BellOutlined, UserOutlined } from "@ant-design/icons";
import Title from "antd/es/typography/Title";
import { useState } from "react";
import { Link } from "react-router-dom";

import CreateButton from "./buttons/create-button";
import SearchInput from "./buttons/search-input";
import UserProfilePopover from "./popovers/UserProfilePopover";
import CompactSearchInput from "./buttons/compact-search-input";

import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import WikiFilterPopover from "./popovers/wiki-filter-popover";

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
const WikiHeader = () => {
  const [showSearchHeader, setSearchHeader] = useState(true);
  const [filters, setFilters] = useState({
    order: "recent",
  });
  const [searchQuery, setSearchQuery] = useState("");
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
    searchParams.append("name", searchQuery);
    searchParams.append("order", filters.order);
    if (isQueryValid(filters.author))
      searchParams.append("author_name", filters.author);
    if (isQueryValid(filters.startDate) || isQueryValid(filters.endDate))
      searchParams.append(
        "creation_date",
        generateDateRange(filters.startDate, filters.endDate)
      );
    searchParams.append("page", 1);


    const searchUrl = `/wikis/search?${searchParams.toString()}`;
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
            <Link to="/">
              <Title level={3} className="header-title wiki-title">
                LaWiki
              </Title>
            </Link>
            {/* Depende de la información que le venga de la ruta */}
          </div>

          <div className="header-tools">
            <SearchInput
              searchPlaceholder={t("wikis.wiki-search-placeholder")}
              toggleHeader={toggleSearchHeader}
              query={searchQuery}
              setQuery={setSearchQuery}
              popover={
                <WikiFilterPopover filters={filters} setFilters={setFilters} />
              }
              searchFunction={searchHandler}
            />
            {!user ? <></> :
              <Link to="/wikis/new">
                <CreateButton text={t("wikis.new-wiki")} />
              </Link>
            }

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
          searchPlaceholder={t("wikis.wiki-search-placeholder")}
          query={searchQuery}
          setQuery={setSearchQuery}
          toggleHeader={toggleSearchHeader}
          popover={
            <WikiFilterPopover filters={filters} setFilters={setFilters} />
          }
          searchFunction={searchHandler}
        />
      )}
    </>
  );
};

export default WikiHeader;
