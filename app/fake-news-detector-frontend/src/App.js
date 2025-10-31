import React from 'react';
import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';

import Home from './components/home';
import NewsQuiz from './components/newsquiz';
import CheckByTitle from './components/checkbytitle';
import CategoryContainer from './components/category';
import Documentation from './components/documentation';
import { MyProvider } from './context';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },

  {
    path: '/newsquiz',
    element: <NewsQuiz />,
  },

  {
    path: '/checkbytitle',
    element: <CheckByTitle />,
  },

  {
    path: '/documentation',
    element: <Documentation />,
  },

  {
    path: '/category/:category',
    element: <CategoryContainer />,

  }
]);

function App() {

  return (
    <React.StrictMode>
      <MyProvider>
        <RouterProvider router={router} />
      </MyProvider>
    </React.StrictMode>
  );
}

export default App;
