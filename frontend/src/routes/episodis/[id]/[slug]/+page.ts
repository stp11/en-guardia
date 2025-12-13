import { error } from "@sveltejs/kit";
import { getEpisodeApiEpisodesIdGet } from "src/client";

import type { PageLoad } from "../$types";

export const load: PageLoad = async ({ params }) => {
  const response = await getEpisodeApiEpisodesIdGet({
    path: {
      id: +params.id,
    },
  });

  if (response.error) {
    throw error(response.response.status);
  }

  return {
    episode: response.data,
  };
};
