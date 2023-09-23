import ReactDOM from 'react-dom'
import App from "./App" // import App functional component from App.jsx file
import './index.css'    // import css styling for whole web page

/* 
   - render React components into the DOM
   - DOM = web page's structure and content representation
   - ReactDOM.render() takes a React component and mounts it onto a specified DOM element
*/
ReactDOM.render(<App/>, document.querySelector("#root"))