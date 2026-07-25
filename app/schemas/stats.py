from pydantic import BaseModel, computed_field


class CampaignStatsResponse(BaseModel):
    total_contacts: int
    total_sent: int
    total_opens: int
    total_clicks: int

    @computed_field
    @property
    def open_rate(self) -> float:
        if self.total_sent == 0:
            return 0.0
        return round((self.total_opens / self.total_sent) * 100, 2)

    @computed_field
    @property
    def click_rate(self) -> float:
        if self.total_sent == 0:
            return 0.0
        return round((self.total_clicks / self.total_sent) * 100, 2)