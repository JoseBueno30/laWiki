import { Button, Grid, Input, Popover, Flex } from "antd";
const { useBreakpoint } = Grid;

import { SearchIcon, FilterIcon } from "../../../utils/icons";
import IconWrapper from "../../../utils/icon-wrapper";
import Icon from "@ant-design/icons";
import WikiFilterPanel from "../popovers/wiki-filter-panel";

const FilterClickHandler = () => {
  console.log("Filter clicked");
};

const wikiTags = ["Tag 1", "Tag 2", "Tag 3", "Tag 4", "Tag 5"];

const SearchButton = ({
  searchPlaceholder,
  filters,
  setFilters,
  query,
  setQuery,
  toggleHeader,
}) => {
  const popover = (
    <Popover
      placement='bottomRight'
      content={
        <WikiFilterPanel
          filters={filters}
          setFilters={setFilters}
          wikiTags={wikiTags}
        />
      }
      trigger="click"
    >
      {/* Debería cambiar en funcion de si es de wiki  */}
      <Flex justify="center" align="center">
        {FilterIcon()}
      </Flex>
    </Popover>
  );

  const screens = useBreakpoint();

  return (
    <>
      {screens.md ? (
        <Input.Search
          placeholder={searchPlaceholder}
          allowClear
          suffix={popover}
          size="large"
          style={{ maxWidth: "300px" }}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      ) : (
        <Button
          variant="outlined"
          icon={SearchIcon()}
          shape="circle"
          onClick={toggleHeader}
        />
      )}
    </>
  );
};

export default SearchButton;
