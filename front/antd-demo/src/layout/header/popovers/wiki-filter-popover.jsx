import { Popover, Flex } from "antd";
import { FilterIcon } from "../../../utils/icons";
import WikiFilterPanel from "./wiki-filter-panel";

const WikiFilterPopover = ({ filters, setFilters}) => {
  return (
    <Popover
      trigger="click"
      overlayStyle={{ width: 350 }}
      content={
        <WikiFilterPanel
          filters={filters}
          setFilters={setFilters}
        />
      }
    >
      {/* Debería cambiar en funcion de si es de wiki  */}
      <Flex justify="center" align="center" className="icon-container">
        {FilterIcon()}
      </Flex>
    </Popover>
  );
};

export default WikiFilterPopover;
