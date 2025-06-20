import React from 'react';
import { ChakraProvider, Box, Container } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import CreateProfile from './pages/CreateProfile';
import VerifyFace from './pages/VerifyFace';
import Profiles from './pages/Profiles';
import theme from './theme';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <Box minH="100vh" bg="gray.50">
          <Navbar />
          <Container maxW="container.xl" py={8}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/create-profile" element={<CreateProfile />} />
              <Route path="/verify" element={<VerifyFace />} />
              <Route path="/profiles" element={<Profiles />} />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ChakraProvider>
  );
}

export default App; 