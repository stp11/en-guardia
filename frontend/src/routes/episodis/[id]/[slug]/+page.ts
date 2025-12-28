import { error, redirect } from "@sveltejs/kit";
import { getEpisodeApiEpisodesIdGet } from "src/client";

import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params }) => {
  const response = await getEpisodeApiEpisodesIdGet({
    path: {
      id: +params.id,
    },
  });

  if (response.error) {
    throw error(response.response.status);
  }

  // Validate slug and redirect to canonical URL if incorrect
  const episode = response.data;
  if (episode?.slug && params.slug !== episode.slug) {
    throw redirect(301, `/episodis/${params.id}/${episode.slug}`);
  }

  return {
    episode: response.data,
  };
};
