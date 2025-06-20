import React from 'react';
import { Box, Button, Heading, Text, SimpleGrid, Icon, VStack } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { FiUserPlus, FiCheck, FiList } from 'react-icons/fi';

const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: FiUserPlus,
      title: 'Create Face Profile',
      description: 'Upload a photo to create a unique face profile with detailed facial measurements.',
      action: () => navigate('/create-profile'),
    },
    {
      icon: FiCheck,
      title: 'Verify Identity',
      description: 'Compare a new photo against existing profiles to verify identity.',
      action: () => navigate('/verify'),
    },
    {
      icon: FiList,
      title: 'View Profiles',
      description: 'Browse and manage all stored face profiles.',
      action: () => navigate('/profiles'),
    },
  ];

  return (
    <Box>
      <VStack spacing={6} textAlign="center" mb={12}>
        <Heading size="2xl" color="brand.700">
          Face Recognition System
        </Heading>
        <Text fontSize="xl" color="gray.600" maxW="2xl">
          A powerful face recognition system that creates detailed profiles and verifies
          identities using advanced facial analysis technology.
        </Text>
      </VStack>

      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8} mt={8}>
        {features.map((feature, index) => (
          <Box
            key={index}
            bg="white"
            p={8}
            borderRadius="lg"
            shadow="md"
            transition="all 0.2s"
            _hover={{ transform: 'translateY(-4px)', shadow: 'lg' }}
          >
            <VStack spacing={4} align="center">
              <Icon as={feature.icon} w={10} h={10} color="brand.500" />
              <Heading size="md" color="brand.700">
                {feature.title}
              </Heading>
              <Text color="gray.600" textAlign="center">
                {feature.description}
              </Text>
              <Button onClick={feature.action} size="lg" width="full">
                Get Started
              </Button>
            </VStack>
          </Box>
        ))}
      </SimpleGrid>
    </Box>
  );
};

export default Home; 