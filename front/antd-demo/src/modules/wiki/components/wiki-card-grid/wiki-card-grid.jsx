import React from "react";
import { Grid,  Flex } from "antd";
import "./wiki-card-grid.css";
import WikiCardItem from "../wiki-card-item/wiki-card-item";

const { useBreakpoint } = Grid;

const WikiCardGrid = ({ wikiList }) => {
  const screens = useBreakpoint();
  return (
    <Flex wrap gap="middle" justify={screens.md ? "start" : "center" }>
      {wikiList.map((wiki) => (
        <WikiCardItem key = {wiki.id} title = {wiki.title} description = {wiki.description} rating = {wiki.rating} image = {wiki.image ?? ""} />
      ))}
    </Flex>
  );
};

export default WikiCardGrid;
