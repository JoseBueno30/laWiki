import { useLocation } from "react-router-dom"
import { Button } from "antd"
import { useContext } from "react"
import { ThemeContext } from "./context/theme-context"

const TestRoute = () => {
    const {colorTheme, toggleTheme} = useContext(ThemeContext)

    let location = useLocation()
    return (
        <div>
            <h1>{location.pathname}</h1>
            <Button onClick={toggleTheme}>
                Toggle theme
            </Button>
        </div>
    )
}

export default TestRoute