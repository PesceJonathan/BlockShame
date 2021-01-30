import * as React from "react";
import styled from "styled-components";
import Switch from "@material-ui/core/Switch";
import boomSwitchStyle from "_utils/boomSwitchStyle";
import { makeStyles } from "@material-ui/core/styles";

const MenuItemStyled = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
`;

const Item = styled.div`
  display: flex;
  flex-direction: column;
`;

const Title = styled.h3``;

const Desc = styled.h4`
  font-weight: 300;
`;

// @ts-ignore
const useStyles = makeStyles(boomSwitchStyle);

interface Props {
  optionName: string;
  optionDescription?: string;
  toggled?: boolean;
}
const MenuItem = (props: Props) => {
  const classes = useStyles(props);
  const [toggled, setToggled] = React.useState(false);

  return (
    <MenuItemStyled>
      <Item>
        <Title>{props.optionName}</Title>
        {props.optionDescription && <Desc>{props.optionDescription}</Desc>}
      </Item>
      <Switch
        classes={classes}
        checked={toggled}
        onChange={(e) => setToggled(e.target.checked)}
      />
    </MenuItemStyled>
  );
};

export default MenuItem;
