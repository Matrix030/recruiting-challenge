import React from 'react';
import { Box, Flex, Button, Heading, Stack } from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <Box bg="white" px={4} shadow="sm">
      <Flex h={16} alignItems="center" justifyContent="space-between" maxW="container.xl" mx="auto">
        <Heading as={RouterLink} to="/" size="md" color="brand.600">
          Validia Face Recognition
        </Heading>

        <Stack direction="row" spacing={4}>
          <Button
            as={RouterLink}
            to="/create-profile"
            variant={isActive('/create-profile') ? 'solid' : 'ghost'}
            colorScheme="brand"
          >
            Create Profile
          </Button>
          <Button
            as={RouterLink}
            to="/verify"
            variant={isActive('/verify') ? 'solid' : 'ghost'}
            colorScheme="brand"
          >
            Verify Face
          </Button>
          <Button
            as={RouterLink}
            to="/profiles"
            variant={isActive('/profiles') ? 'solid' : 'ghost'}
            colorScheme="brand"
          >
            Profiles
          </Button>
        </Stack>
      </Flex>
    </Box>
  );
};

export default Navbar; 