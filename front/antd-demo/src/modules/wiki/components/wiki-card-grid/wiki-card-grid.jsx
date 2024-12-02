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
        <WikiCardItem wiki = {wiki} />
      ))}
    </Flex>
  );
};

export default WikiCardGrid;
