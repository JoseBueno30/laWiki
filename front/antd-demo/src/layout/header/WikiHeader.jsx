import React from "react";
import {
  Flex,
  Input,
  Button,
  Badge,
  Avatar,
  Popover,
} from "antd";
import {
  ControlOutlined,
  PlusOutlined,
  BellOutlined,
  UserOutlined,
} from "@ant-design/icons";
import Title from "antd/es/typography/Title";
import { Link } from "react-router-dom";
import UserProfilePopover from "./UserProfilePopover";
import "./PageHeader.css";

const FilterIcon = () => {
  return (
    <div className="icon-container" onClick={FilterClickHandler}>
      <ControlOutlined style={{ fontSize: "24px" }} />
    </div>
  );
};

const AddIcon = () => <PlusOutlined />;

const NotificationsClickHandler = () => {
  console.log("Notifications clicked");
};

const FilterClickHandler = () => {
  console.log("Filter clicked");
};

const LaWikiClickHandler = () => {
  console.log("LaWiki clicked");
};

const WikiClickHandler = () => {
  console.log("Wiki clicked");
};

const WikiHeader = () => {
  return (
    <>
      <Flex gap="large">
        <Link to="/">
          <Title
            style={{ marginTop: "0.5em" }}
            onClick={LaWikiClickHandler}
            className="header-title"
          >
            LaWiki
          </Title>
        </Link>
        <Title style={{ marginTop: "0.5em" }}>/</Title>
        <Title
          style={{ marginTop: "0.5em" }}
          onClick={WikiClickHandler}
          className="header-title"
        >
          JoJoWiki
        </Title>
      </Flex>

      <Flex gap={50}>
        <Input.Search
          placeholder="search for articles"
          allowClear
          suffix={FilterIcon()}
          size="large"
          style={{ width: "400px" }}
        />
        <Button
          variant="outlined"
          icon={AddIcon()}
          iconPosition="start"
          size={"large"}
        >
          New article
        </Button>
        <Badge count={9} size="large">
          <div className="icon-container" onClick={NotificationsClickHandler}>
            <BellOutlined style={{ fontSize: "24px" }} />
          </div>
        </Badge>
        <Popover
          content={<UserProfilePopover />}
          trigger="click"
          placement="bottomRight"
          overlayStyle={{ width: 260 }}
        >
          <Avatar size="large" icon={<UserOutlined />} />
        </Popover>
      </Flex>
    </>
  );
};


export default WikiHeader;
