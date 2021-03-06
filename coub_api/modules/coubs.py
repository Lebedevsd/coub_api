from typing import List

from coub_api.modules.base import TmpBaseConnector, connector_return_type
from coub_api.schemas.coub import BigCoub
from coub_api.schemas.constants import VisibilityType

__all__ = ("Coubs",)


class Coubs(TmpBaseConnector):
    __slots__ = ()

    def _get_coub_response(self, coub_id: str) -> connector_return_type:
        url = self.build_url(f"/coubs/{coub_id}")
        return self.request("get", url)

    def get_coub(self, coub_id: str) -> BigCoub:
        return BigCoub(**self._get_coub_response(coub_id).json())

    def _edit_coub_response(
        self,
        coub_permalink: str,
        channel_id: int,
        *,
        title: str,
        tags: List[str],
        visibility_type: VisibilityType,
    ) -> connector_return_type:
        url = self.build_url(f"/coubs/{coub_permalink}/update_info")
        params = {
            "coub[channel_id]": channel_id,
            "coub[title]": title,
            "coub[tags]": ",".join(tags),
            "coub[original_visibility_type]": visibility_type,
        }
        return self.authenticated_request("post", url, params=params)

    def edit_coub(
        self,
        coub_permalink: str,
        channel_id: int,
        *,
        title: str,
        tags: List[str],
        visibility_type: VisibilityType = VisibilityType.PRIVATE,
    ) -> BigCoub:
        data = self._edit_coub_response(
            coub_permalink,
            channel_id,
            title=title,
            tags=tags,
            visibility_type=visibility_type,
        )
        return BigCoub(**data.json())

    def delete_coub(self, coub_permalink: str):
        raise NotImplementedError

    # see https://coub.com/dev/docs/Coub+API%2FCreating+coub
    def init_upload(self):
        url = self.build_url("/coubs/init_upload")
        return self.authenticated_request("post", url).json()

    def upload_video(
        self, coub_id: int, video_path: str, content_type: str = "video/mp4"
    ):
        # content_types:
        # https://gist.github.com/Derfirm/5b11f77d64816153024e979141b69800
        url = self.build_url(f"/coubs/{coub_id}/upload_video")
        headers = {"Content-type": content_type}
        return self.authenticated_request(
            "post", url, data=open(video_path, "rb"), headers=headers
        ).json()

    def upload_audio(
        self, coub_id: int, audio_path: str, content_type: str = "audio/mpeg"
    ):
        # content_types:
        # https://gist.github.com/Derfirm/5b11f77d64816153024e979141b69800
        headers = {"Content-type": content_type}
        url = self.build_url(f"/coubs/{coub_id}/upload_audio")
        return self.authenticated_request(
            "post", url, data=open(audio_path, "rb"), headers=headers
        ).json()

    def finalize_upload(
        self,
        coub_id: int,
        *,
        title: str,
        tags: List[str],
        visibility_type: VisibilityType = VisibilityType.PRIVATE,
        sound_enabled: bool = True,
    ):
        url = self.build_url(f"/coubs/{coub_id}/finalize_upload")
        params = {
            "sound_enabled": sound_enabled,
            "title": title,
            "original_visibility_type": visibility_type,
            "tags": ",".join(tags),
        }
        return self.authenticated_request("post", url, params=params).json()

    def get_upload_status(self, coub_id: int):
        url = self.build_url(f"/coubs/{coub_id}/finalize_status")
        return self.authenticated_request("get", url).json()
