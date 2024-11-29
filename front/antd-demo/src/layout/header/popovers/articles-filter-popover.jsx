import { Popover, Flex } from "antd";
import { FilterIcon } from "../../../utils/icons";
import ArticlesFilterPanel from "./articles-filter-panel";

const ArticlesFilterPopover = ({ filters, setFilters, wikiTags }) => {
  return (
    <Popover
      trigger="click"
      overlayStyle={{ width: 350 }}
      content={
        <ArticlesFilterPanel
          filters={filters}
          setFilters={setFilters}
          wikiTags={wikiTags}
        />
      }
    >
      {/* Debería cambiar en funcion de si es de wiki  */}
      <Flex justify="center" align="center">
        {FilterIcon()}
      </Flex>
    </Popover>
  );
};

export default ArticlesFilterPopover;
