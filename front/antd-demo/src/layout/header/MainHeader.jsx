import "./PageHeader.css";
import { Flex, Badge, Avatar, Popover, Grid } from "antd";
import {
  BellOutlined,
  UserOutlined,
} from "@ant-design/icons";
import Title from "antd/es/typography/Title";
import { useState } from "react";
import { Link } from "react-router-dom";

import CreateButton from "./buttons/create-button";
import SearchInput from "./buttons/search-input";
import UserProfilePopover from "./popovers/UserProfilePopover";
import CompactSearchInput from "./buttons/compact-search-input";

import { useTranslation } from "react-i18next";
import WikiFilterPopover from "./popovers/wiki-filter-popover";

const NotificationsClickHandler = () => {
  console.log("Notifications clicked");
};

// Aqui seguramente se pase la informacion de la wiki, como el nombre, id y tags.
const WikiHeader = () => {
  const [showSearchHeader, setSearchHeader] = useState(true);
  const [filters, setFilters] = useState({
    order: "recent",
    author: "",
    startDate: "2024/01/01",
  });
  const [searchQuery, setSearchQuery] = useState("");
  const { t } = useTranslation('header');

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
              <Title level={3} className="header-title wiki-title">
                LaWiki
              </Title>
            </Link>
            {/* Depende de la información que le venga de la ruta */}
          </div>

          <div className="header-tools">
            <SearchInput
              searchPlaceholder={t('wiki-search-placeholder')}
              toggleHeader={toggleSearchHeader}
              query={searchQuery}
              setQuery={setSearchQuery}
              popover={
                <WikiFilterPopover
                  filters={filters}
                  setFilters={setFilters}
                />
              }
              searchFunction={() => console.log("Searching...")}
            />
            <CreateButton text={t('new-wiki')} />
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
          searchPlaceholder={t('wiki-search-placeholder')}
          query={searchQuery}
          setQuery={setSearchQuery}
          toggleHeader={toggleSearchHeader}
          popover={
            <WikiFilterPopover
              filters={filters}
              setFilters={setFilters}
            />
          }
          searchFunction={() => console.log("Searching...")}
        />
      )}
    </>
  );
};

export default WikiHeader;
