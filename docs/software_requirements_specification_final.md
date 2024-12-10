#  Overview
This document serves as the Software Requirements Specification (SRS) for the system. It outlines the system's functional and non-functional requirements, providing a detailed framework for its development, testing, and deployment. The purpose is to ensure all stakeholders have a clear understanding of what the system will do and the constraints under which it will operate.


# Software Requirements
This section is divided into Functional Requirements and Non-Functional Requirements. For clarity and traceability, each requirement is categorized under specific system features or aspects.

## Functional Requirements

### <User Account Management>
| ID | Requirement |
| :-------------: | :----------: |
| FR1 | The system shall allow users to create an account, log in, and manage their profile.> |
| FR2 | Users shall be able to update their preferences and interests (e.g., genre, actors, languages). |
| FR3 | The system shall provide users with a search function to look up specific movies or actors. |
| FR4 | The system shall allow users to save or bookmark movies for future viewing. |
| FR5 | Users shall be able to rate or provide feedback on recommendations (e.g., thumbs up, thumbs down, or review). |

### <Recommendation System>
| ID | Requirement |
| :-------------: | :----------: |
| FR6 | Users shall be able to submit feedback on previous recommendations to improve future suggestions. |
| FR7 | The system shall generate a list of personalized movie recommendations based on user inputs. |
| FR8 | The system shall allow users to refine their suggestions by applying filters (e.g., genre, rating, or release date). |
| FR9 | Users shall be able to choose the streaming platforms they prefer for recommendations. |
| FR10 | The system shall check and display where each recommended movie can be watched (e.g., Netflix, Amazon Prime, Hulu). |

### <Movie Information and Interaction>
| ID | Requirement |
| :-------------: | :----------: |
| FR11 | The system shall display detailed information about recommended movies, including title, genre, cast, rating, and synopsis. |
| FR12 | The system shall provide a sneak peek or trailer of each movie. |
| FR13 | The system shall support movie lists based on user categories (e.g., watch later, favorites). |
| FR14 | The system shall allow users to share movie recommendations with others through social media. |
| FR15 | The system shall include a feature to notify users about new releases or updates in their selected genres. |

## Non-Functional Requirements

### <System Performance and Scalability>

| ID | Requirement |
| :-------------: | :----------: |
| NFR1 | The system should respond to user input and generate movie recommendations within 2 seconds. |
| NFR2 | The system should support up to 1,000 concurrent users without performance degradation. |
| NFR3 | The system must be able to scale horizontally to handle increased load as the user base grows. |
| NFR4 | The system should have 99.9% uptime to ensure recommendations are always available to users. |
| NFR5 | The system should be resilient and able to recover from failures automatically. |

### <Compatibility and Usability>

| ID | Requirement |
| :-------------: | :----------: |
| NFR6 | The user interface should be intuitive, easy to navigate, and accessible on both desktop and mobile devices. |
| NFR7 | The system should provide a seamless experience with clear instructions for user input. |
| NFR8 | The system should be compatible with operating systems (Windows, macOS, Android, iOS). |
| NFR9 | The system should use responsive design principles for optimal performance across devices. |
| NFR10 | The system should provide visual cues or tips to guide new users during their first interaction. |

### <Security and Data Integrity>

| ID | Requirement |
| :-------------: | :----------: |
| NFR11 | User data (such as login credentials and preferences) shall be encrypted both at rest and in transit. |
| NFR12 | The system shall implement user authentication mechanisms to ensure only authorized access. |
| NFR13 | The system shall log all access attempts and provide an audit trail for security reviews. |
| NFR14 | The system shall comply with GDPR and other applicable data protection regulations. |
| NFR15 | The system shall enforce session timeouts and two-factor authentication for added security. |

# Software Artifacts

This section outlines the various artifacts related to the system that serve as deliverables or documentation supporting development, testing, and deployment.

* [Jira Board](https://wlfz.atlassian.net/jira/software/projects/WT/boards/2)
* [Use Case Diagram](https://github.com/laurenbrown14/GVSU-CIS350-WLFZ/blob/main/artifacts/use_case_diagram/use_case_diagram.pdf)
