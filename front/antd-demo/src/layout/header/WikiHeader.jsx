import { Flex, Input, Button, Badge, Avatar, Grid, Space } from "antd";
import { BellOutlined, UserOutlined, CloseOutlined } from "@ant-design/icons";
import "./PageHeader.css";
import Title from "antd/es/typography/Title";
import { FilterIcon } from "../../utils/icons";
import { useState } from "react";
const { useBreakpoint } = Grid;
import { Link } from "react-router-dom";

import CreateButton from "./buttons/create-button";
import SearchButton from "./buttons/search-button";

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

const WikiHeader = () => {
  const screens = useBreakpoint();
  const [showSearchHeader, setSearchHeader] = useState(true);

  const [filters, setFilters] = useState({
    order: 'recent',
    tags: [],
    author: '',
    editor: '',
  });
  const [searchQuery, setSearchQuery] = useState("");

  const toggleSearchHeader = () => {
    setSearchHeader(!showSearchHeader);
  };

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
            <SearchButton
              searchPlaceholder="search for articles"
              toggleHeader={toggleSearchHeader}
              filters={filters}
              setFilters={setFilters}
              query={searchQuery}
              setQuery={setSearchQuery}
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
        <Space.Compact style={{ width: "100%" }}>
          <Button
            size="large"
            icon={<CloseOutlined />}
            onClick={toggleSearchHeader}
          />
          <Input.Search
            placeholder="search for articles"
            allowClear
            suffix={FilterIcon()}
            size="large"
          />
        </Space.Compact>
      )}
    </>
  );
};

export default WikiHeader;
