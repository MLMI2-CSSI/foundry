from pydantic import AnyUrl, ValidationError, BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum


class DataciteIdentifier(BaseModel):
    
    class DataciteIdentifierType(Enum):
        DOI="DOI"
    
    identifier: str = ""
    identifierType: DataciteIdentifierType

class DataciteCreator(BaseModel):
    creatorName: str = ""
    nameIdentifiers: Optional[str] = ""
    affiliations : Optional[List[str]]= []
    familyName: Optional[str] = ""
    givenName: Optional[str] = ""

class DataciteTitle(BaseModel):
    
    class DataciteTitleType(Enum):
        AlternativeTitle = "AlternativeTitle"
        Subtitle = "Subtitle"
        TranslatedTitle = "TranslatedTitle"
        Other = "Other"
    
    title: str = ""
    type: Optional[DataciteTitleType]
    lang: Optional[str]

class DataciteSubject(BaseModel):
    subject : str = ""
    subjectScheme : Optional[str] = ""
    schemeURI: Optional[AnyUrl] = ""
    valueURI: Optional[AnyUrl] = ""
    lang : str = ""

class DataciteResourceTypeGeneral(Enum):
    Audiovisual = "Audiovisual"
    Collection = "Collection"
    Dataset = "Dataset"
    Event = "Event"
    Image = "Image"
    InteractiveResource = "InteractiveResource"
    Model = "Model"
    PhysicalObject = "PhysicalObject"
    Service = "Service"
    Software = "Software"
    Sound = "Sound"
    Text = "Text"
    Workflow = "Workflow"
    Other = "Other"

class DataciteResourceType(BaseModel):
    resourceType : Optional[str] = ""
    resourceTypeGeneral: DataciteResourceTypeGeneral = None

class DataciteContributor(BaseModel):
    
    class DataciteContributorType(Enum):
        ContactPerson = "ContactPerson"
        DataCollector = "DataCollector"
        DataCurator = "DataCurator"
        DataManager = "DataManager"
        Editor = "Editor"
        HostingInstitution = "HostingInstitution"
        Other = "Other"
        Producer = "Producer"
        ProjectLeader = "ProjectLeader"
        ProjectManager = "ProjectManager"
        ProjectMember = "ProjectMember"
        RegistrationAgency = "RegistrationAgency"
        RegistrationAuthority = "RegistrationAuthority"
        RelatedPerson = "RelatedPerson"
        ResearchGroup = "ResearchGroup"
        RightsHolder = "RightsHolder"
        Researcher = "Researcher"
        Sponsor = "Sponsor"
        Supervisor = "Supervisor"
        WorkPackageLeader = "WorkPackageLeader"
        
    contributorType: DataciteContributorType = None
    contributorName: str = ""
    affiliations: Optional[List[str]] = []
    familyName: Optional[str] = ""
    givenName: Optional[str] = ""
    
class DataciteAlternateIdentifier(BaseModel):
    alternateIdentifier: str = ""
    alternateIdentifierType : str = ""

class DataciteRelatedIdentifier(BaseModel):
    
    class DataciteRelatedIdentifierType(Enum):
        ARK = "ARK"
        arXiv = "arXiv"
        bibcode = "bibcode"
        DOI = "DOI"
        EAN13 = "EAN13"
        EISSN = "EISSN"
        Handle = "Handle"
        IGSN = "IGSN"
        ISBN = "ISBN"
        ISSN = "ISSN"
        ISTC = "ISTC"
        LISSN = "LISSN"
        LSID = "LSID"
        PMID = "PMID"
        PURL = "PURL"
        UPC = "UPC"
        URL = "URL"
        URN = "URN"
        
    class DataciteRelationType(Enum):
        IsCitedBy = "IsCitedBy"
        Cites = "Cites"
        IsSupplementTo = "IsSupplementTo"
        IsSupplementedBy = "IsSupplementedBy"
        IsContinuedBy = "IsContinuedBy"
        Continues = "Continues"
        IsNewVersionOf = "IsNewVersionOf"
        IsPreviousVersionOf = "IsPreviousVersionOf"
        IsPartOf = "IsPartOf"
        HasPart = "HasPart"
        IsReferencedBy = "IsReferencedBy"
        References = "References"
        IsDocumentedBy = "IsDocumentedBy"
        Documents = "Documents"
        IsCompiledBy = "IsCompiledBy"
        Compiles = "Compiles"
        IsVariantFormOf = "IsVariantFormOf"
        IsOriginalFormOf = "IsOriginalFormOf"
        IsIdenticalTo = "IsIdenticalTo"
        HasMetadata = "HasMetadata"
        IsMetadataFor = "IsMetadataFor"
        Reviews = "Reviews"
        IsReviewedBy = "IsReviewedBy"
        IsDerivedFrom = "IsDerivedFrom"
        IsSourceOf = "IsSourceOf"
        
    relatedIdentifer : str = ""
    relatedIdentiferType : DataciteRelatedIdentifierType = None
    relatedMetadataScheme: str = ""
    schemeURI : AnyUrl = "" 
        
class Datacite(BaseModel):
    identifier: DataciteIdentifier
    creators: List[DataciteCreator] = []
    titles: List[DataciteTitle] = []
    publisher : str = ""
    publicationYear : str = ""
    subjects : List[DataciteSubject]
    resourceType : Optional[DataciteResourceType] = None
    contributors : List[DataciteContributor] = []
    language: Optional[str] = None
    resourceType: DataciteResourceType = None
    alternateIdentifiers : List[DataciteAlternateIdentifier] = []
    relatedIdentifiers: List[DataciteRelatedIdentifier] = []

    __datacite_version : Optional[str] = "4.3"

    def to_json(self, exclude_unset=True):
        return self.json(exclude_unset=exclude_unset)

    def to_xml(self):
        pass
    
    def describe(self):
        print("Datacite version: {}".format(self.__datacite_version))