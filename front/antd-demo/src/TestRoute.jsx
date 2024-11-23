import { useLocation } from "react-router-dom"
import { Button } from "antd"
import { useContext } from "react"
import { ThemeContext } from "./context/theme-context"

import ArticleList from "./modules/articles/components/article-list/article-list";

const TestRoute = () => {
    const {colorTheme, toggleTheme} = useContext(ThemeContext)

    

    let location = useLocation()
    return (
        <>
        
        <div>
            <h1>{location.pathname}</h1>
            <Button onClick={toggleTheme}>
                Toggle theme
            </Button>
            <ArticleList articleList={article}/>
        </div>
        </>
    )
}

export default TestRoute