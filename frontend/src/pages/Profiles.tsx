import React, { useEffect, useState } from 'react';
import {
  Box,
  Heading,
  Text,
  VStack,
  SimpleGrid,
  Card,
  CardBody,
  Button,
  Spinner,
  useToast,
} from '@chakra-ui/react';
import { listProfiles } from '../services/api';

const Profiles = () => {
  const [profiles, setProfiles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const toast = useToast();

  const fetchProfiles = async () => {
    try {
      const response = await listProfiles((page - 1) * 12, 12);
      if (response.length < 12) {
        setHasMore(false);
      }
      if (page === 1) {
        setProfiles(response);
      } else {
        setProfiles(prev => [...prev, ...response]);
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to load profiles. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfiles();
  }, [page]);

  const loadMore = () => {
    setPage(prev => prev + 1);
  };

  if (loading && page === 1) {
    return (
      <Box textAlign="center" py={20}>
        <Spinner size="xl" color="brand.500" />
      </Box>
    );
  }

  return (
    <Box>
      <VStack spacing={8} align="stretch">
        <Box textAlign="center">
          <Heading size="xl" color="brand.700" mb={4}>
            Face Profiles
          </Heading>
          <Text fontSize="lg" color="gray.600">
            Browse all stored face profiles and their measurements.
          </Text>
        </Box>

        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
          {profiles.map(profile => (
            <Card key={profile.id}>
              <CardBody>
                <VStack align="stretch" spacing={3}>
                  <Heading size="md" color="brand.700">
                    Profile #{profile.id}
                  </Heading>
                  <Text color="gray.600" noOfLines={4}>
                    {profile.description}
                  </Text>
                  <Text fontSize="sm" color="gray.500">
                    Created: {new Date(profile.created_at).toLocaleString()}
                  </Text>
                </VStack>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>

        {hasMore && (
          <Button
            onClick={loadMore}
            isLoading={loading}
            size="lg"
            variant="outline"
            mx="auto"
          >
            Load More
          </Button>
        )}

        {!hasMore && profiles.length > 0 && (
          <Text textAlign="center" color="gray.500">
            No more profiles to load.
          </Text>
        )}

        {profiles.length === 0 && (
          <Box textAlign="center" py={10}>
            <Text fontSize="lg" color="gray.500">
              No profiles found. Create one to get started!
            </Text>
          </Box>
        )}
      </VStack>
    </Box>
  );
};

export default Profiles; 