import React from "react";
import { Flex } from "antd";
import "./wiki-card-grid.css";
import WikiCardItem from "../wiki-card-item/wiki-card-item";

const WikiCardGrid = ({ wikiList }) => {
  return (
    <Flex wrap gap="middle">
      {wikiList.map((wiki) => (
        <WikiCardItem key = {wiki.id} title = {wiki.title} description = {wiki.description} rating = {wiki.rating} image = {wiki.image ?? ""} />
      ))}
    </Flex>
  );
};

export default WikiCardGrid;
