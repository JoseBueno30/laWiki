import { Flex, Input, Button, Badge, Avatar, Grid, Space } from "antd";
import {
  ControlOutlined,
  PlusOutlined,
  BellOutlined,
  UserOutlined,
  CloseOutlined,
} from "@ant-design/icons";
import PropTypes from "prop-types";
import "./PageHeader.css";
import Title from "antd/es/typography/Title";
import CreateButton from "./buttons/create-button";
import SearchButton from "./buttons/search-button";

import { useState } from "react";

const { useBreakpoint } = Grid;

const FilterClickHandler = () => {
  console.log("Filter clicked");
}

const FilterIcon = () => {
  return (
    <div className="icon-container" onClick={FilterClickHandler}>
      <ControlOutlined style={{ fontSize: "24px" }} />
    </div>
  )
}

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

  const toggleSearchHeader = () => {
    setSearchHeader(!showSearchHeader);
  };

  return (
    <>
      {showSearchHeader ? (
        <>
          <div className="header-title-container">
            <Title
              level={3}
              style={{ marginTop: "0.5em" }}
              onClick={LaWikiClickHandler}
              className="header-title"
            >
              LaWiki
            </Title>
            {/* Depende de la información que le venga de la ruta */}

            <Title level={3} style={{ marginTop: "0.5em" }} className="header-title">
              /
            </Title>
            <Title
              level={3}
              style={{ marginTop: "0.5em", maxWidth: "200px" }}
              onClick={WikiClickHandler}
              className="header-title wiki-title"
            >
              JoJoWikideddedededdedededededddded
            </Title>
          </div>

          <div className="header-tools">
            <SearchButton toggleHeader={toggleSearchHeader} />
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
              <Avatar size='default' icon={<UserOutlined />} />
            </div>
          </div>
        </>
      ) : (
        <Space.Compact style={{width: "100%"}}>
          <Button
            shape="round"
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

WikiHeader.propTypes = {
  children: PropTypes.node,
};

export default WikiHeader;
