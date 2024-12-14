import { Tabs } from "antd";
import WikiCardGrid from "../../../wiki/components/wiki-card-grid/wiki-card-grid";
import { useState } from "react";

const UserContent = ({articles=[], wikis=[]}) => {

    console.log(articles);
    
    console.log(wikis);

    const content_wikis = <WikiCardGrid wikiList={wikis}/>;

    return(<Tabs
    centered
    items={[
        { "label": "Wikis",
            "key": 1,
            "children": content_wikis
        },
        { "label": "Articles",
            "key": 2,
            "children": <p>{articles}</p>
    }]}/>);
};
export default UserContent;