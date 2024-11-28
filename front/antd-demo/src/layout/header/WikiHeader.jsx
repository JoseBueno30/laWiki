import { Flex, Input, Button, Badge, Avatar, Grid, Space } from "antd";
import { BellOutlined, UserOutlined, CloseOutlined } from "@ant-design/icons";
import "./PageHeader.css";
import Title from "antd/es/typography/Title";
import { FilterIcon } from "../../utils/icons";
import { useState } from "react";
const { useBreakpoint } = Grid;
import { Link } from "react-router-dom";

import CreateButton from "./buttons/create-button";
import SearchInput from "./buttons/search-input";
import ArticlesFilterPopover from "./popovers/articles-filter-popover";
import CompactSearchInput from "./buttons/compact-search-input";

const ProfileClickHandler = () => {
  console.log("Profile clicked");
};

const NotificationsClickHandler = () => {
  console.log("Notifications clicked");
};

const LaWikiClickHandler = () => {
  console.log("LaWiki clicked");
};

const WikiClickHandler = () => {
  console.log("Wiki clicked");
};

// Aqui seguramente se pase la informacion de la wiki, como el nombre, id y tags.
const WikiHeader = () => {
  const screens = useBreakpoint();
  const [showSearchHeader, setSearchHeader] = useState(true);
  const wikiTags = ["Tag 1", "Tag 2", "Tag 3", "Tag 4", "Tag 5"];
  const [filters, setFilters] = useState({
    order: "recent",
    tags: [],
    author: "",
    editor: "",
    startDate: "2024/01/01",
  });
  const [searchQuery, setSearchQuery] = useState("");

  const toggleSearchHeader = () => {
    setSearchHeader(!showSearchHeader);
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
              <Title
                level={3}
                onClick={LaWikiClickHandler}
                className="header-title wiki-title"
              >
                LaWiki
              </Title>
            </Link>
            {/* Depende de la información que le venga de la ruta */}

            <Title level={3} className="header-title">
              /
            </Title>
            <Title
              level={3}
              onClick={WikiClickHandler}
              className="header-title wiki-title"
            >
              JoJoWikideddedededdedededededddded
            </Title>
          </div>

          <div className="header-tools">
            <SearchInput
              searchPlaceholder="search for articles"
              toggleHeader={toggleSearchHeader}
              query={searchQuery}
              setQuery={setSearchQuery}
              popover={
                <ArticlesFilterPopover
                  filters={filters}
                  setFilters={setFilters}
                  wikiTags={wikiTags}
                />
              }
              searchFunction={() => console.log("Searching...")}
            />
            <CreateButton text="Create Article" />
            <Badge count={9} size="large">
              <div
                className="icon-container"
                onClick={NotificationsClickHandler}
              >
                <BellOutlined style={{ fontSize: "24px" }} />
              </div>
            </Badge>
            <div className="icon-container" onClick={ProfileClickHandler}>
              <Avatar size="default" icon={<UserOutlined />} />
            </div>
          </div>
        </>
      ) : (
        <CompactSearchInput
          searchPlaceholder="search for articles"
          query={searchQuery}
          setQuery={setSearchQuery}
          toggleHeader={toggleSearchHeader}
          popover={
            <ArticlesFilterPopover
              filters={filters}
              setFilters={setFilters}
              wikiTags={wikiTags}
            />
          }
          searchFunction={() => console.log("Searching...")}
        />
      )}
    </>
  );
};

export default WikiHeader;
