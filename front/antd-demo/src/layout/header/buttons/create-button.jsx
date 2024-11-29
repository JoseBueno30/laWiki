import { Button, Grid } from "antd";
const { useBreakpoint } = Grid;

import { AddIcon } from "../../../utils/icons";

const CreateButton = ({ text }) => {
  const screens = useBreakpoint();

  return (
    <>
      {screens.md ? (
        <Button
          variant="outlined"
          icon={AddIcon()}
          iconPosition="start"
          size={"large"}
        >
          {text}
        </Button>
      ) : (
        <Button
          variant="outlined"
          icon={AddIcon()}
          shape="circle"
        />
      )}
    </>
  );
};

export default CreateButton;